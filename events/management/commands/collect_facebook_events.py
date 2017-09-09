from django.core.management.base import BaseCommand, CommandError
import facebook
from django.conf import settings
from datetime import datetime, timedelta
import re
from events.models import FacebookEvent, FacebookPlace
from pprint import pprint
from psycopg2 import IntegrityError

class Command(BaseCommand):
    help = 'Reads facebook data and saves events in DB'

    GRAPH = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN, \
        version=settings.FACEBOOK_GRAPH_API_VERSION)
    FACEBOOK_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

    def save_page(self, page_data):

        # 1444427242532563?fields=about,name,picture
        page = self.GRAPH.get_object(page_id, fields='about,name,picture')
        pass

    def save_location(self, location_data):
        print('LOCATION')
        pprint(location_data)
        if ('location' not in location_data) or ('latitude' not in location_data['location']) or ('longitude' not in location_data['location']):
            return None
        location_dict = {
            'latitude':  location_data['location']['latitude'],
            'longitude':  location_data['location']['longitude'],
            'facebook_name': location_data['name'],
            'facebook_id': location_data.get('id',''),
            'facebook_city':  location_data['location']['city'],
            'facebook_country':  location_data['location']['country'],
            'facebook_street':  location_data['location'].get('street',''),
            'facebook_zip':  location_data['location'].get('zip',''),
        }
        try:
            fb_place = FacebookPlace.objects.get(facebook_id=location_data['id'])
        except KeyError as e:
            print('KEY ERROR')
            fb_place = FacebookPlace.objects.create(**location_dict)
        except FacebookPlace.DoesNotExist:
            fb_place = FacebookPlace.objects.create(**location_dict)
        fb_place.save()
        return fb_place

    def save_event(self, event_id):
        self.stdout.write('Saving event')
        event_data = self.GRAPH.get_object(id=event_id)
        print('CREATED')
        pprint(event_data)
        start = datetime.strptime(event_data['start_time'], self.FACEBOOK_DATETIME_FORMAT)
        # if the event has already passed we skip it
        # if start.timestamp() < datetime.now().timestamp():
        #     return
        # we only care about events that can be mapped
        if 'place' not in event_data:
            return

        location = self.save_location(event_data['place'])
        if not location:
            self.stdout.write(self.style.NOTICE('Skipping Event - No Location'))
            return None
        fb_fields = {
            'facebook_id': event_data['id'],
            'name': event_data['name'],
            'description': event_data['description'],
            'start_time': datetime.strptime(event_data['start_time'], self.FACEBOOK_DATETIME_FORMAT),
            'facebook_place': location,
        }
        # if 'end_time' in event_data:
        #     print('end time', event_data['end_time'])
        #     fb_fields['end_time'] = datetime.strptime(event_data['end_time'], self.FACEBOOK_DATETIME_FORMAT),
        try:
            fb_event = FacebookEvent.objects.get(facebook_id = event_id)
            for key,value in fb_fields.items():
                setattr(fb_event, key, value)
            return
        except FacebookEvent.DoesNotExist:
            fb_event = FacebookEvent.objects.create(**fb_fields)
            fb_event.save()


        # event_image = graph.get_connections(event_id, 'picture', fields="url")

        # admins = graph.get_connections(event_id, 'admins', fields='profile_type')
        # for admin in admins:
        #     if admin['data']['profile_type'] is 'page':
        #         save_page(page)

        # if event['start_time'] is in future:
            # save event
        self.stdout.write('Saving event {}'.format(event_data))
        return

    def handle(self, *args, **kwargs):
        # bullshit group
        group_id = '1814445198866527'
        # NYC Free Standup group
        group_id = '209897822492693'
        # connections = graph.get_connections(group_id, 'feed', fields='link,message')
        # this gets every connection ever

        last = datetime.now() - timedelta(days=30)
        timestamp = round(last.timestamp())



        connections = self.GRAPH.get_all_connections(group_id, 'feed', fields='link,message,message_tags',since=timestamp)
        # event_regex = 'facebook\.com\/events\/(.+)\/'
        for index, connection in enumerate(connections):
            pprint(connection)
            print(index)
            for item in ['link', 'message']:
                # match for event urls and capture the ID
                if item not in connection:
                    continue
                match_obj = re.search(r'facebook\.com\/events\/(.+)\/', connection[item])
                print('match', match_obj, connection[item])
                if match_obj and match_obj.group(1):
                    self.save_event(match_obj.group(1))
            if 'message_tags' in connection:
                for tag in connection['message_tags']:
                    if 'type' in tag and tag['type'] is 'event':
                        self.save_event(tag['id'])


        self.stdout.write(self.style.SUCCESS('All done :)'))
