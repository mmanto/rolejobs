# -*- coding: utf8 -*-

from __future__ import unicode_literals
import logging

from django.views.decorators.csrf import csrf_exempt
from django.views import generic

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

    id = int(request.data.get("id"))
    hash = request.data.get("hash")

    try:
        user = User.objects.get(id=id)
    except:
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


##########
# Forms
##########

class ChangePasswordFormView(generic.FormView):
    template_name = 'account_change_password.html'
    form_class = NgChangePasswordForm
