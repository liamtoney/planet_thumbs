import os
import json
from planet import api
import requests

# BASIC OPTIONS ----------------------------------------------------------------
VOLCANO = 'shishaldin'
# Maximum allowable fraction of cloud cover [0-1]
MAX_CLOUD_COVER = 0
# Maximum number of thumbnails to grab
NUM_THUMBNAILS = 5
# ------------------------------------------------------------------------------

# ADVANCED OPTIONS -------------------------------------------------------------
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
# Must be valid JSON!
VOLCANO_COORDINATES_FILE = 'avo_volcanoes.json'
# ------------------------------------------------------------------------------

api_key = os.getenv('PL_API_KEY')

with open(VOLCANO_COORDINATES_FILE) as f:
    summit_coordinates = json.load(f)

volcano_lowercase = VOLCANO.lower()
try:
    coordinates = summit_coordinates[volcano_lowercase][::-1]
except KeyError:
    print(f'Volcano "{volcano_lowercase}" not found. Possible options are:')
    [print(f'\t{volcano}') for volcano in summit_coordinates.keys()]
    raise

aoi = {
    "type": "Point",
    "coordinates": coordinates
}

client = api.ClientV1()

query = api.filters.and_filter(
    api.filters.geom_filter(aoi),
    api.filters.range_filter('cloud_cover', lte=MAX_CLOUD_COVER)
)

request = api.filters.build_search_request(query, ITEM_TYPES)
results = client.quick_search(request)

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
    print(filename)
    with open(filename, 'wb') as f:
        f.write(response.content)
