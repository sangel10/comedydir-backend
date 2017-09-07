from django.core.management.base import BaseCommand, CommandError
import facebook
from django.conf import settings

class Command(BaseCommand):
    help = 'Reads facebook data and saves events in DB'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        graph = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN,
            version=settings.FACEBOOK_GRAPH_API_VERSION)
        event_id = '1961159624142597'
        event = graph.get_object(id=event_id)
        # for poll_id in options['poll_id']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()

        self.stdout.write('{}'.format(event))
        self.stdout.write(self.style.SUCCESS('It worked'))
