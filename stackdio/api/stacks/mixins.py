# -*- coding: utf-8 -*-

# Copyright 2016,  Digital Reasoning
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from stackdio.core.mixins import ParentRelatedMixin
from stackdio.core.permissions import (
    StackdioPermissionsPermissions,
    StackdioPermissionsObjectPermissions,
)
from . import models


class StackRelatedMixin(ParentRelatedMixin):
    parent_queryset = models.Stack.objects.all()

    def get_stack(self):
        return self.get_parent_object()


class StackPermissionsMixin(StackRelatedMixin):
    permission_classes = (StackdioPermissionsPermissions,)
    parent_permission_classes = (StackdioPermissionsObjectPermissions,)

    def get_permissioned_object(self):
        return self.get_parent_object()
