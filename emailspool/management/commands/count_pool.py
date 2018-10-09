from django.core.management.base import BaseCommand, CommandError

from emailspool.models import Spool

class Command(BaseCommand):
    args = ''
    help = 'Get number of email in the pool'

    def handle(self, *args, **options):

        cant = Spool.objects.filter(sent=False).count()
        self.stdout.write("%i emails for send\n" % cant)
