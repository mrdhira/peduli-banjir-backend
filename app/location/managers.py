import logging
import certifi
import ssl
import geopy.geocoders
import pickle
from geopy.geocoders import Nominatim
from django.db import transaction
from django.db.models import Manager, Q
from app.utils.redis import redis_client as cache

logger = logging.getLogger(__name__)

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

LOCATION_GEOLOCATOR_RESP_KEY = "location_geolocator_resp_{}_{}"


class LocationManager(Manager):
    def get_location(self, latitude, longtitude):
        geolocation = cache.get(
            LOCATION_GEOLOCATOR_RESP_KEY.format(latitude, longtitude)
        )

        if not geolocation:
            geolocator = Nominatim(user_agent="dwigata.putra@gmail.com")
            geolocation = geolocator.reverse(f"{latitude}, {longtitude}")

            logger.info("response from geolocator")
            print(geolocation)

            cache.set(
                LOCATION_GEOLOCATOR_RESP_KEY.format(latitude, longtitude),
                pickle.dumps(geolocation),
                600,  # 10 Min
            )
        else:
            geolocation = pickle.loads(geolocation)

        country_code = geolocation.raw["address"].get("country_code", "")
        country = geolocation.raw["address"].get("country", "")
        state = geolocation.raw["address"].get("state", "")
        city = geolocation.raw["address"].get("city", "")
        city_district = geolocation.raw["address"].get("city_district", "")
        village = geolocation.raw["address"].get("village", "")
        residential = geolocation.raw["address"].get("residential", "")
        postal_code = geolocation.raw["address"].get("postcode", "")
        address = geolocation.raw.get("display_name", "")

        print("==============")
        print(country_code)
        print(country)
        print(state)
        print(city)
        print(city_district)
        print(village)
        print(residential)
        print(postal_code)
        print(address)
        print("==============")

        if country_code != "":
            location = self.filter(country_code=country_code)

        if country != "":
            location = self.filter(country=country)

        if state != "":
            location = self.filter(state=state)

        if city != "":
            location = self.filter(city=city)

        if city_district != "":
            location = self.filter(city_district=city_district)

        if village != "":
            location = self.filter(village=village)

        if residential != "":
            location = self.filter(residential=residential)

        if postal_code != "":
            location = self.filter(postal_code=postal_code)

        if address != "":
            location = self.filter(address=address)

        location = self.first()

        print("==============")
        print(location)
        print("==============")

        if not location:
            with transaction.atomic():
                location = self.create(
                    country_code=country_code,
                    country=country,
                    state=state,
                    city=city,
                    city_district=city_district,
                    village=village,
                    residential=residential,
                    address=address,
                )

        return location
