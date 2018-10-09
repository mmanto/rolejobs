from django.core.management.base import BaseCommand, CommandError

from emailspool.models import Spool

class Command(BaseCommand):
    args = ''
    help = 'Process a part of email pool'

    def handle(self, *args, **options):

        self.stdout.write("[Email Spool] Starting pool work\n")

        for mail in Spool.get_pool():
            mail.send()
            if mail.status == Spool.S_SUCCESS:
                status = 'Success'
            else:
                status = 'Fail (%s)' % mail.error

            self.stdout.write("[Email Spool] Send email to %s id: %i has %s\n" % (mail.to, mail.id, status))

        self.stdout.write("[Email Spool] Pool work finished\n")
