from pyproj import Geod
from planet import api
import requests

VOLCANO = 'shishaldin'

AOI_RADIUS_KM = 1

PL_API_KEY = os.getenv('PL_API_KEY')

M_PER_KM = 1000

SUMMIT_COORDINATES = {
    'shishaldin': (54.7554, -163.9711),
    'pavlof': (55.4173, -161.8937)
}

lat_0, lon_0 = SUMMIT_COORDINATES[VOLCANO.lower()]

g = Geod(ellps='WGS84')

lon_min, _, _ = g.fwd(lon_0, lat_0, 270, AOI_RADIUS_KM * M_PER_KM)
lon_max, _, _ = g.fwd(lon_0, lat_0, 90, AOI_RADIUS_KM * M_PER_KM)
_, lat_min, _ = g.fwd(lon_0, lat_0, 180, AOI_RADIUS_KM * M_PER_KM)
_, lat_max, _ = g.fwd(lon_0, lat_0, 0, AOI_RADIUS_KM * M_PER_KM)

aoi = {
  "type": "Point",
  "coordinates": [

      lon_0, lat_0,
      # [lon_max, lat_min],
      # [lon_max, lat_max],
      # [lon_min, lat_max],
      # [lon_min, lat_min]

  ]
}

query = api.filters.and_filter(
    api.filters.geom_filter(aoi),
    api.filters.range_filter('cloud_cover', lt=0.1)
)

item_types = ['PSScene3Band', 'PSScene4Band']
request = api.filters.build_search_request(query, item_types)
results = client.quick_search(request)

for item in results.items_iter(5):
    thumbnail_url = item['_links']['thumbnail']
    response = requests.get(thumbnail_url, auth=(PL_API_KEY, ''),
                           params=dict(width=2048))
    with open('{}.png'.format(item['properties']['acquired']), 'wb') as f:
        f.write(response.content)
