# from django.core.management.base import BaseCommand, CommandError
# import facebook
# from django.conf import settings
# from datetime import datetime, timedelta
#
#
# class Command(BaseCommand):
#     help = 'Reads facebook data and saves events in DB'
#
#     # def add_arguments(self, parser):
#     #     parser.add_argument('poll_id', nargs='+', type=int)
#
#
#     def save_page(self, page_data):
#
#         # 1444427242532563?fields=about,name,picture
#         page = graph.get_object(page_id, fields='about,name,picture')
#         pass
#
#
#     def save_event(self, event_data):
#         # admins = graph.get_connections(event_id, 'admins', fields='profile_type')
#         # for admin in admins:
#         #     if admin['data']['profile_type'] is 'page':
#         #         save_page(page)
#
#         # if event['start_time'] is in future:
#             # save event
#         pass
#
#     def handle(self):
#         graph = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN, \
#             version=settings.FACEBOOK_GRAPH_API_VERSION)
#         # event_id = '1961159624142597'
#         # event = graph.get_object(id=event_id)
#         # Comedy Directory
#         # https://www.facebook.com/groups/1814445198866527/
#         group_id = '1814445198866527'
#
#         # connections = graph.get_connections(group_id, 'feed', fields='link,message')
#         # this gets every connection ever
#
#         last = datetime.now() - timedelta(days=30)
#         timestamp = round(last.timestamp())
#
#         connections = graph.get_all_connections(group_id, 'feed', fields='link,message',since=timestamp)
#         for connection in connections:
#             if 'facebook.com/events/' in connection['link']:
#                 self.save_event(connection)
#
#
#
#         # self.stdout.write('{}'.format(event))
#         self.stdout.write(self.style.SUCCESS('It worked'))
