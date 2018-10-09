# encoding=utf-8

from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from rest_framework import generics
from rest_framework.response import Response

from emailspool.models import Spool

from serializers import ContactSerializer
from forms import ContactForm


class ContactView(generics.GenericAPIView):
    """Signup new postulant"""

    serializer_class = ContactSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = Spool.create_by_layout('contact_email', request.data)

        email.to = settings.CONTACT_EMAIL
        email.subject = _('[CONTACTO] %s' % request.data["subject"])
        email.reply_to = request.data["email"]
        email.save()

        return Response({"success": _("Sent")})


class ContactFormView(generic.FormView):
    template_name = 'contact_form.html'
    form_class = ContactForm
