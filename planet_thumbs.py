import sys
import os
import json
from planet import api
import requests

# Maximum allowable fraction of cloud cover [0-1]
MAX_CLOUD_COVER = 0

# Maximum number of thumbnails to grab
NUM_THUMBNAILS = 5

# See https://developers.planet.com/docs/data/items-assets/#item-types
ITEM_TYPES = [
    'PSScene3Band',
    'PSScene4Band',
    'PSOrthoTile',
    'REOrthoTile',
    'REScene',
    'SkySatScene',
    'SkySatCollect',
    'Landsat8L1G',
    'Sentinel2L1C'
]

# [px] See https://developers.planet.com/docs/data/item-previews/#size
IMAGE_WIDTH = 2048

# Must be valid JSON and in the same directory as this script!
VOLCANO_COORDINATES_FILE = 'avo_volcanoes.json'

if len(sys.argv) != 2:
    raise TypeError('Please specify a (single) volcano!')
volcano = sys.argv[1]

api_key = os.getenv('PL_API_KEY')

script_dir = os.path.dirname(__file__)
with open(os.path.join(script_dir, VOLCANO_COORDINATES_FILE)) as f:
    summit_coordinates = json.load(f)

volcano_lowercase = volcano.lower()
try:
    coordinates = summit_coordinates[volcano_lowercase][::-1]
except KeyError:
    print(f'Volcano "{volcano_lowercase}" not found. Possible options are:\n')
    [print(f'\t{volcano}') for volcano in summit_coordinates.keys()]
    print()
    raise

client = api.ClientV1()

query = api.filters.and_filter(
    api.filters.geom_filter(dict(type='Point', coordinates=coordinates)),
    api.filters.range_filter('cloud_cover', lte=MAX_CLOUD_COVER)
)

request = api.filters.build_search_request(query, ITEM_TYPES)
results = client.quick_search(request)

filenames = []
for item in results.items_iter(NUM_THUMBNAILS):
    thumbnail_url = item['_links']['thumbnail']
    response = requests.get(thumbnail_url, auth=(api_key, ''),
                            params=dict(width=IMAGE_WIDTH))
    filename = '_'.join([volcano_lowercase,
                         item['properties']['acquired'],
                         item['properties']['item_type']
                         ])
    filename = filename.replace('.', '_')
    filename = filename.replace(':', '_')
    filename += '.png'
    # If we'd overwrite existing files, append a "0" to the filename
    if filename in filenames:
        filename = filename.split('.')[0] + '0' + '.png'
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(filename)
    filenames.append(filename)
