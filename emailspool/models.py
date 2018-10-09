import datetime

from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import get_template
from django.template import Context


class Spool(models.Model):
    """Spool Mail"""

    S_NEW = 0x00
    S_SUCCESS = 0x01
    S_ERROR = 0x02
    S_SENDIND = 0x03
    S_DISCARTED = 0x04

    AVAILABLE_STATUS = (
        (S_NEW, "New"),
        (S_SUCCESS, "Sent"),
        (S_ERROR, "With errors"),
        (S_SENDIND, "Sending"),
        (S_DISCARTED, "Discarted")
    )

    from_name = models.CharField(
            max_length=250, null=True, blank=True, default=None)
    reply_to = models.EmailField(null=True, blank=True, default=None)
    to = models.EmailField()
    priority = models.SmallIntegerField(default=0)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False, db_index=True)
    sent_date = models.DateTimeField(null=True, default=None)
    status = models.SmallIntegerField(null=False, default=S_NEW)
    error = models.CharField(
            max_length=8192, null=True, default=None, blank=True)
    errors = models.SmallIntegerField(null=False, default=0)

    def send(self):

        self.status = self.S_SENDIND

        text_body = strip_tags(self.content)
        headers = {}

        if self.reply_to:
            headers['Reply-To'] = self.reply_to

        if self.from_name:
            mail_from = "%s <%s>" % (self.from_name, settings.EMAIL_FROM)
        else:
            mail_from = settings.EMAIL_FROM

        email = EmailMultiAlternatives(
                self.subject,
                text_body,
                mail_from,
                (self.to,),
                headers=headers)

        email.attach_alternative(self.content, "text/html")
        try:
            email.send()
        except Exception as  e:

            if self.errors > 5:
                self.status = self.S_DISCARTED
            else:
                self.status = self.S_ERROR

            self.errors = self.errors + 1
            self.error = str(e)
            self.priority = self.priority + 10
            self.save()
        else:
            self.sent = True
            self.sent_date = datetime.datetime.today()
            self.status = self.S_SUCCESS
            self.save()

    @classmethod
    def get_pool(cls, cant=10):

        pool = cls.objects.filter(
                sent=False).filter(
                        status__in=(cls.S_NEW, cls.S_ERROR)).order_by(
                            'priority')[0:10]

        for work in pool:
            yield work

    @classmethod
    def get_context(self, params):

        own_params = params.copy()

        own_params.update({
            "base_url": settings.SITE_BASE_URL
        })

        return Context(own_params)

    @classmethod
    def create_by_layout(cls, layout_name, params={}):
        layout = get_template('emails/%s.html' % layout_name)
        html = layout.render(cls.get_context(params))

        mail = cls()
        mail.content = html

        return mail
