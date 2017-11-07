from django.core.management.base import BaseCommand, CommandError
import facebook
from django.conf import settings
from datetime import datetime, timedelta
import re
from events.models import FacebookEvent, FacebookPlace, FacebookGroup, FacebookPage
from pprint import pprint
from psycopg2 import IntegrityError
from decimal import Decimal
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    help = 'Reads facebook data and saves events in DB'

    GRAPH = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN, \
        version=settings.FACEBOOK_GRAPH_API_VERSION)
    # MOVE THIS TO CONSTANTS
    FACEBOOK_DATETIME_FORMAT = settings.FACEBOOK_DATETIME_FORMAT

    def save_page(self, page_data):
        page = self.GRAPH.get_object(page_id, fields='about,name,picture')

    def save_location(self, location_data):
        if ('location' not in location_data) or ('latitude' not in location_data['location']) or ('longitude' not in location_data['location']):
            return None

        fb_place = None
        if not location_data.get('id',''):
            return fb_place
        try:
            fb_place = FacebookPlace.objects.get(
                facebook_id=location_data.get('id',''),
            )
        except FacebookPlace.DoesNotExist as e:
            try:
                # DecimalField doesn't always give an exact match, so we add some padding to catch
                # inexact numbers
                offset = 0.000002
                fb_place = FacebookPlace.objects.get(
                    latitude__gte=(location_data['location']['latitude'] - offset),
                    latitude__lte=(location_data['location']['latitude'] + offset),
                    longitude__gte=(location_data['location']['longitude'] - offset),
                    longitude__lte=(location_data['location']['longitude'] + offset),
                )
            except FacebookPlace.DoesNotExist as e:
                place_data = self.GRAPH.get_object(location_data['id'], fields='name,id,location{latitude,longitude,city,street,zip,country,region}')
                location_dict = {
                    'facebook_name': place_data['name'],
                    'facebook_id': place_data['id'],
                    'latitude':  place_data['location']['latitude'],
                    'longitude':  place_data['location']['longitude'],
                    'point': Point(place_data['location']['latitude'], place_data['location']['longitude']),
                    'facebook_city':  place_data['location'].get('city', ''),
                    'facebook_country':  place_data['location'].get('country', ''),
                    'facebook_street':  place_data['location'].get('street',''),
                    'facebook_zip':  place_data['location'].get('zip',''),
                    'facebook_region':  place_data['location'].get('region',''),
                }
                fb_place = FacebookPlace.objects.create(**location_dict)
                fb_place.save()
        return fb_place

    def save_event(self, event_id):
        try:
            event_data = self.GRAPH.get_object(id=event_id, fields='id,name,description,start_time,end_time,place,cover')
        except facebook.GraphAPIError as e:
            self.stdout.write(self.style.WARNING('Skipping event {}'.format(e)))
            return
        start = datetime.strptime(event_data['start_time'], self.FACEBOOK_DATETIME_FORMAT)
        # if the event has already passed we skip it
        # if start.timestamp() < datetime.now().timestamp():
        #     return
        # we only care about events that can be mapped
        if 'place' not in event_data:
            return

        try:
            fb_event = FacebookEvent.objects.get(facebook_id = event_id)
            self.stdout.write('Existing event {} - {}'.format(event_data['name'], event_data['id']))
            return fb_event
        except FacebookEvent.DoesNotExist:
            pass

        location = self.save_location(event_data['place'])
        if not location:
            self.stdout.write(self.style.NOTICE('Skipping Event - No Location {}').format(event_data['place']))
            return None
        fb_fields = {
            'facebook_id': event_data['id'],
            'name': event_data['name'],
            'description': event_data.get('description', ' '),
            'start_time': datetime.strptime(event_data['start_time'], self.FACEBOOK_DATETIME_FORMAT),
            'facebook_place': location,
        }
        if 'cover' in event_data:
            fb_fields['image_url'] = event_data['cover']['source']

        # if 'end_time' in event_data:
        #     print('end time', event_data['end_time'])
        #     fb_fields['end_time'] = datetime.strptime(event_data['end_time'], self.FACEBOOK_DATETIME_FORMAT),
        try:
            fb_event = FacebookEvent.objects.get(facebook_id = event_id)
            for key,value in fb_fields.items():
                setattr(fb_event, key, value)
        except FacebookEvent.DoesNotExist:
            fb_event = FacebookEvent.objects.create(**fb_fields)
        fb_event.save()
        # admins = graph.get_connections(event_id, 'admins', fields='profile_type')
        # for admin in admins:
        #     if admin['data']['profile_type'] is 'page':
        #         save_page(page)

        # if event['start_time'] is in future:
            # save event
        self.stdout.write('Saving event {} - {}'.format(event_data['name'], event_data['id']))
        return fb_event

    def get_posts_from_groups(self):
        days = 10
        last_month = datetime.now() - timedelta(days=days)
        since_timestamp = round(last_month.timestamp())
        for group in FacebookGroup.objects.all():
            group_id = group.facebook_id
            try:
                connection = self.GRAPH.get_object(id=group_id, fields='name')
            except facebook.GraphAPIError as e:
                self.stdout.write(self.style.WARNING('Skipping group {}'.format(e)))
                continue
            group.name = connection['name']
            group.save()
            connections = self.GRAPH.get_all_connections(group_id, 'feed', fields='link,message,message_tags', since=since_timestamp)
            for index, connection in enumerate(connections):
                for item in ['link', 'message']:
                    # match for event urls and capture the ID
                    if item not in connection:
                        continue
                    match_obj = re.search(r'facebook\.com\/events\/(.+)\/', connection[item])
                    if match_obj and match_obj.group(1):
                        self.save_event(match_obj.group(1))
                if 'message_tags' in connection:
                    for tag in connection['message_tags']:
                        if 'type' in tag and tag['type'] is 'event':
                            self.save_event(tag['id'])
    def get_pages_from_post(self):
        comments = self.GRAPH.get_all_connections(1824334737877573, "comments", fields='message,message_tags')
        for c in comments:
            print(c)
            message = c.get('message', None)
            # TODO: for now we just assume the message is a url pointing to a FB page
            if not message:
                continue
            if 'facebook.com/' in message:
                match_obj = re.search(r'facebook\.com\/(.+)\/', message)
                if match_obj and match_obj.group(1):
                    page_id = match_obj.group(1)
                    print('MATCH', match_obj.group(1))
                    # page = self.GRAPH.get_object(id=page_id, fields="name, about")
                    try:
                        page = self.GRAPH.get_object(id="https%3A//facebook.com/{}".format(page_id),fields="name,about")
                    except Exception as e:
                        print(e)
                        continue

                    print('PAGe', page)
                    fb_page, created = FacebookPage.objects.get_or_create(facebook_id=page_id)
                    fb_page.about = page.get('about')
                    fb_page.name = page.get('name')
                    fb_page.save()


        # import pdb; pdb.set_trace()

    def get_events_from_pages(self):
        for page in FacebookPage.objects.all():
            last_month = datetime.now() - timedelta(days=30)
            since_timestamp = round(last_month.timestamp())
            try:
                object_exists = self.GRAPH.get_object(id=page.facebook_id)
            except facebook.GraphAPIError as e:
                print('CAUGHT ERROR', e)
                continue
            connections = self.GRAPH.get_all_connections(page.facebook_id, 'events', fields='link,message,message_tags',since=since_timestamp)
            for c in connections:
                print('EVENT', c)
                self.save_event(c.get('id'))

    def handle(self, *args, **kwargs):
        self.get_posts_from_groups()
        self.get_pages_from_post()
        self.get_events_from_pages()
        self.stdout.write(self.style.SUCCESS('All done :)'))
