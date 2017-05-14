# -*- coding: utf-8 -*-

# Copyright 2017,  Digital Reasoning
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

from __future__ import print_function, unicode_literals

import logging

from django.apps import AppConfig
from django.db import DEFAULT_DB_ALIAS
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from stackdio.core.constants import Events
from stackdio.core.models import Event

logger = logging.getLogger(__name__)


def create_event_tags(app_config, verbosity=2, interactive=True,
                      using=DEFAULT_DB_ALIAS, **kwargs):

    if not app_config.models_module:
        return

    for tag in Events.ALL:
        # Create the event tag if it doesn't exist
        Event.objects.using(using).get_or_create(tag=tag)


class CoreConfig(AppConfig):
    name = 'stackdio.core'
    verbose_name = _('stackd.io Core')

    def ready(self):
        post_migrate.connect(create_event_tags, sender=self)
