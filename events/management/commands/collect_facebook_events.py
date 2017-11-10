
from datetime import datetime, timedelta
import re
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.conf import settings
import facebook
from events.models import FacebookEvent, FacebookPlace, FacebookGroup, FacebookPage

class Command(BaseCommand):
    help = 'Reads facebook data and saves events in DB'

    GRAPH = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN, \
        version=settings.FACEBOOK_GRAPH_API_VERSION)
    # MOVE THIS TO CONSTANTS
    FACEBOOK_DATETIME_FORMAT = settings.FACEBOOK_DATETIME_FORMAT

    def save_location(self, location_data):
        if ('location' not in location_data) or ('latitude' not in location_data['location']) or ('longitude' not in location_data['location']):
            return None

        fb_place = None
        if not location_data.get('id', ''):
            return fb_place
        try:
            fb_place = FacebookPlace.objects.get(
                facebook_id=location_data.get('id', ''),
            )
        except FacebookPlace.DoesNotExist:
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
            except FacebookPlace.DoesNotExist:
                place_data = self.GRAPH.get_object(location_data['id'], fields='name,id,location{latitude,longitude,city,street,zip,country,region}')
                location_dict = {
                    'facebook_name': place_data['name'],
                    'facebook_id': place_data['id'],
                    'latitude':  place_data['location']['latitude'],
                    'longitude':  place_data['location']['longitude'],
                    'point': Point(place_data['location']['latitude'], place_data['location']['longitude']),
                    'facebook_city':  place_data['location'].get('city', ''),
                    'facebook_country':  place_data['location'].get('country', ''),
                    'facebook_street':  place_data['location'].get('street', ''),
                    'facebook_zip':  place_data['location'].get('zip', ''),
                    'facebook_region':  place_data['location'].get('region', ''),
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
        # start = datetime.strptime(event_data['start_time'], self.FACEBOOK_DATETIME_FORMAT)
        # if the event has already passed we skip it
        # if start.timestamp() < datetime.now().timestamp():
        #     return
        # we only care about events that can be mapped
        if 'place' not in event_data:
            return

        try:
            fb_event = FacebookEvent.objects.get(facebook_id=event_id)
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

        try:
            fb_event = FacebookEvent.objects.get(facebook_id=event_id)
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
        days = 60
        last_month = datetime.now() - timedelta(days=days)
        since_timestamp = round(last_month.timestamp())
        for group in FacebookGroup.objects.all():
            group_id = group.facebook_id
            try:
                connection = self.GRAPH.get_object(id=group_id, fields='name')
            except facebook.GraphAPIError as e:
                self.stdout.write(self.style.WARNING('Skipping group {}'.format(e)))
                continue
            self.stdout.write(self.style.WARNING('Getting events for group {}'.format(group.name)))
            group.name = connection['name']
            group.save()
            connections = self.GRAPH.get_all_connections(group_id, 'feed', fields='link,message,message_tags', since=since_timestamp)
            for index, connection in enumerate(connections):
                for item in ['link', 'message']:
                    # match for event urls and capture the ID
                    if item not in connection:
                        continue
                    # print('TL post', connection[item])
                    match_obj = re.search(r'facebook\.com\/events\/(.+)\/', connection[item])
                    if match_obj and match_obj.group(1):
                        self.save_event(match_obj.group(1))
                if 'message_tags' in connection:
                    for tag in connection['message_tags']:
                        if 'type' in tag and tag['type'] == 'event':
                            self.save_event(tag['id'])


    def save_page(self, page_id):
        try:
            page = self.GRAPH.get_object(id="https%3A//facebook.com/{}".format(page_id), fields="name,about")
        except Exception as e:
            print(e)
            return None

        fb_page, created = FacebookPage.objects.get_or_create(facebook_id=page_id)
        fb_page.about = page.get('about')
        fb_page.name = page.get('name')
        fb_page.save()

    def get_events_from_pages(self):
        for page in FacebookPage.objects.all():
            last_month = datetime.now() - timedelta(days=30)
            since_timestamp = round(last_month.timestamp())
            try:
                object_exists = self.GRAPH.get_object(id=page.facebook_id)
            except facebook.GraphAPIError as e:
                continue
            connections = self.GRAPH.get_all_connections(page.facebook_id, 'events', fields='link,message,message_tags', since=since_timestamp)
            for c in connections:
                self.save_event(c.get('id'))


    def save_group(self, group_id):
        try:
            group = FacebookGroup.objects.get(facebook_id=group_id)
            return group
        except FacebookGroup.DoesNotExist:
            try:
                connection = self.GRAPH.get_object(id=group_id, fields='name')
                group = FacebookGroup.objects.create(facebook_id=group_id, name=connection['name'])
                return group
            except facebook.GraphAPIError as e:
                self.stdout.write(self.style.WARNING('Group not readable id:{} - {}'.format(group_id, e)))
                return None


    def get_data_from_root_group(self):
        days = 90
        last_month = datetime.now() - timedelta(days=days)
        since_timestamp = round(last_month.timestamp())
        group_id = settings.FACEBOOK_GROUP_ID
        self.save_group(group_id)

        connections = self.GRAPH.get_all_connections(group_id, 'feed', fields='link,message,message_tags', since=since_timestamp)
        for index, connection in enumerate(connections):
            for item in ['link', 'message']:
                # match for event urls and capture the ID
                if item not in connection:
                    continue
                match_obj = re.search(r'facebook\.com\/events\/(.+)\/', connection[item])
                if match_obj and match_obj.group(1):
                    self.save_event(match_obj.group(1))
                    continue
                match_obj = re.search(r'facebook\.com\/groups\/(.+)\/', connection[item])
                if match_obj and match_obj.group(1):
                    self.save_group(match_obj.group(1))
                    continue
                match_obj = re.search(r'facebook\.com\/(.+)\/', connection[item])
                if match_obj and match_obj.group(1):
                    self.save_page(match_obj.group(1))
                    continue

            if 'message_tags' in connection:
                for tag in connection['message_tags']:
                    if 'type' in tag and tag['type'] == 'event':
                        self.save_event(tag['id'])
                        continue
                    if 'type' in tag and tag['type'] == 'group':
                        self.save_group(tag['id'])
                        continue
                    if 'type' in tag and tag['type'] == 'page':
                        self.save_page(tag['id'])
                        continue


    def handle(self, *args, **kwargs):
        self.get_data_from_root_group()
        self.get_posts_from_groups()
        # self.get_events_from_pages()
        self.stdout.write(self.style.SUCCESS('All done :)'))
