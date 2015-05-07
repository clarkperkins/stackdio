# -*- coding: utf-8 -*-

# Copyright 2014,  Digital Reasoning
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, views
from rest_framework.response import Response

from .exceptions import BadRequest
from . import models, serializers


class UserListAPIView(generics.ListAPIView):
    queryset = get_user_model().objects.exclude(username__in=('__stackdio__', 'AnonymousUser'))
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.exclude(username__in=('__stackdio__', 'AnonymousUser'))
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserSettingsDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.UserSettings.objects.all()
    serializer_class = serializers.UserSettingsSerializer

    def get_object(self):
        return self.request.user.settings


class ChangePasswordAPIView(views.APIView):
    """
    API that handles changing your account password. Note that
    only PUT requests are available on this endpoint. Below
    are the required parameters of the JSON object you will PUT.

    @curent_password: Your current password.
    @new_password: Your new password you want to change to.
    @confirm_password: Confirm your new password.
    """

    def put(self, request, *args, **kwargs):
        current_password = request.DATA.get('current_password')
        new_password = request.DATA.get('new_password')
        confirm_password = request.DATA.get('confirm_password')

        errors = []
        if not current_password:
            errors.append('Current password field is required.')
        if not new_password:
            errors.append('New password field is required.')
        if not confirm_password:
            errors.append('New password confirmation field is required.')
        if errors:
            raise BadRequest(dict(errors=errors))

        if not request.user.check_password(current_password):
            errors.append('You entered an incorrect current password value.')
        if new_password != confirm_password:
            errors.append('Your new password and password confirmation fields '
                          'do not match.')
        if errors:
            raise BadRequest(dict(errors=errors))

        # change the password
        request.user.set_password(new_password)
        request.user.save()

        return Response()


class VersionAPIView(views.APIView):
    """
    Returns a JSON object with version-specific fields.
    """

    def get(self, request, *args, **kwargs):
        from _version import __version__

        return Response({
            'version': __version__,
        })
