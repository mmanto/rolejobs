# -*- coding: utf8 -*-

from __future__ import unicode_literals
import logging

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views import generic
from django.http import JsonResponse

from django.core.mail import send_mail
from django.conf import settings
from emailspool.models import Spool
from django.http import JsonResponse

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.forms import NgChangePasswordForm

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(["POST"])
def validate_account(request):
    """
    Validate an account,
    On this steep, the role is defined
    @TODO get the role
    """

    mid = int(request.data.get("id"))
    hash = request.data.get("hash")

    try:
        user = User.objects.get(id=mid)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:

        if user.status == user.S_NEW:

            if user.check_validation_code(hash):
                user.status = user.S_ENABLED
                user.save()
                logger.debug("Confirmed")
                return Response({
                    "success": True
                }, status.HTTP_200_OK)
            else:
                logger.debug("Validation hash not match")
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            logger.debug("User isn't new")
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class LoginViewset(viewsets.ReadOnlyModelViewSet):
    """Get current user information"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


@csrf_exempt
@api_view(["POST"])
def verify_reset_pass_email(request):
    try:
        email = Spool.objects.filter(to=request.data['email'], sent=False)[0]
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.data['email'], ]
        send_mail(email.subject, email.content, email_from, recipient_list, html_message=email.content)
        email.sent = True
        email.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


def postulation_auth_check(request):
    try:
        User.objects.get(id=request.user.id)
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False})

##########
# Forms
##########

class ChangePasswordFormView(generic.FormView):
    template_name = 'account_change_password.html'
    form_class = NgChangePasswordForm
