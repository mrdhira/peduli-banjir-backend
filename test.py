import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

geolocator = Nominatim(user_agent="http")
location = geolocator.reverse("-6.9859339, 107.6062359")
# print(location)
# print(location.address)
print(location.raw)
# print(location.raw["address"])
# print(location.raw["address"]["city"])

# Kota Baru Parahyangan, Cimahi, Jawa Barat, 40714, Indonesia
# Kota Baru Parahyangan, Cimahi, Jawa Barat, 40714, Indonesia
# {
#     'place_id': 195611965,
#     'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
#     'osm_type': 'way',
#     'osm_id': 412602082,
#     'lat': '-6.876110077330089',
#     'lon': '107.47079801915457',
#     'display_name': 'Kota Baru Parahyangan, Cimahi, Jawa Barat, 40714, Indonesia',
#     'address': {
#         'residential': 'Kota Baru Parahyangan',
#         'city': 'Cimahi',
#         'state': 'Jawa Barat',
#         'postcode': '40714',
#         'country': 'Indonesia',
#         'country_code': 'id'
#     },
#     'boundingbox': [
#         '-6.8761236',
#         '-6.8760884',
#         '107.4686305',
#         '107.4732601'
#     ]
# }
# {
#   "place_id":220297371,
#   "licence":"Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
#   "osm_type":"way",
#   "osm_id":569175875,
#   "lat":"-6.306253259531996",
#   "lon":"106.7346274506868",
#   "display_name":"Kedaung, Pamulang, Tangerang Selatan, Banten, 15413, Indonesia",
#   "address":{
#     "village":"Kedaung", # kelurahan
#     "city_district":"Pamulang", # kecamatan
#     "city":"Tangerang Selatan",
#     "state":"Banten",
#     "postcode":"15413",
#     "country":"Indonesia",
#     "country_code":"id"
#   },
#   "boundingbox":[
#     "-6.3065675",
#     "-6.306157",
#     "106.7346199",
#     "106.7346521"
#   ]
# }
