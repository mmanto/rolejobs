from django.core.management.base import BaseCommand, CommandError

from emailspool.models import Spool

class Command(BaseCommand):
    args = 'to'
    help = 'Create a test email to send'

    def handle(self, *args, **options):

        if args:
            to = args[0]
        else:
            raise CommandError("to is required")

        email = Spool()
        email.subject = "Test email"
        email.content = "<h1>Test Email</h1>\n<p>This is a testing email</p>"
        email.to = to
        email.from_name = "Tester sender"
        email.save()
        self.stdout.write("Emails create, use python manage.py process_pool for send it\n")
