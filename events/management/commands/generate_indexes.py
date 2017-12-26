from django.conf import settings
from django.core.management.base import BaseCommand

from events.models import FacebookPlace, CitiesIndex
import googlemaps

class Command(BaseCommand):
    help = 'Reads facebook data and saves events in DB'

    def handle(self, *args, **kwargs):
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAP_API_KEY)

        places = []
        countries = FacebookPlace.objects.all().order_by().values('facebook_country').distinct()
        for country in countries:
            country_name = country['facebook_country']
            cities = FacebookPlace.objects.filter(facebook_country=country_name).order_by().values('facebook_city', 'facebook_region').distinct()
            for city in cities:
                city_name = city['facebook_city']
                region_name = city['facebook_region']
                print(city_name, region_name, country_name)
                if not city_name or not country_name:
                    continue
                geocode_result = gmaps.geocode("{}, {} {}\n".format(city_name, region_name, country_name))
                # import pdb; pdb.set_trace()
                if not geocode_result[0]:
                    continue
                location = geocode_result[0]['geometry']['location']
                place = {
                    'city': city_name,
                    'country': country_name,
                    'region': region_name,
                    'latitude': location['lat'],
                    'longitude': location['lng']
                }
                places.append(place)

        sorted_places = sorted(places, key=lambda place: "{}{}{}".format(place['country'], place['country'], place['city']))
        CitiesIndex.objects.create(data=sorted_places)
        self.stdout.write(self.style.SUCCESS('All done :)'))
