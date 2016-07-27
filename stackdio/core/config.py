# -*- coding: utf-8 -*-

# Copyright 2016,  Digital Reasoning
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

import getpass
import os

import yaml
from django.core.exceptions import ImproperlyConfigured
from django.utils.crypto import get_random_string
from jinja2 import Template


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'


class StackdioConfig(dict):
    CONFIG_LOCATIONS = (
        '/etc/stackdio/stackdio.yaml',
        'config/stackdio.yaml',
        '~/.stackdio/server.yaml',
    )

    REQUIRED_FIELDS = (
        'user',
        'database_url',
        'storage_dir',
        'log_dir',
        'django_secret_key',
        'create_ssh_users',
        'salt_bootstrap_args',
    )

    DEFAULT_CONTEXT = {
        'user': getpass.getuser(),
        'random_secret_key': get_random_string(50, SECRET_CHARS),
    }

    def __init__(self):
        super(StackdioConfig, self).__init__()
        self.cfg_file = None
        self._load_stackdio_config()

    def _load_stackdio_config(self):
        for cfg_file in self.CONFIG_LOCATIONS:
            cfg_file = os.path.expanduser(cfg_file)
            cfg_file = os.path.join(BASE_DIR, cfg_file)
            if os.path.isfile(cfg_file):
                self.cfg_file = cfg_file
                break

        if self.cfg_file is None:
            raise ImproperlyConfigured(
                'Missing stackdio configuration file. '
                'To create the file, you may use `stackdio init`'
            )

        with open(self.cfg_file) as f:
            template = Template(f.read())
            stackdio_config = yaml.safe_load(template.render(**self.DEFAULT_CONTEXT))

        if not stackdio_config:
            raise ImproperlyConfigured(
                'stackdio configuration file appears to be empty or not valid yaml.'
            )

        errors = []
        for k in self.REQUIRED_FIELDS:
            if k not in stackdio_config:
                errors.append('Missing parameter `{0}`'.format(k))

        if errors:
            msg = 'stackdio configuration errors:\n'
            for err in errors:
                msg += '  - {0}\n'.format(err)
            raise ImproperlyConfigured(msg)

        self.update(stackdio_config)

        self.storage_dir = os.path.join(BASE_DIR, self.storage_dir)

        # Try to create the storage dir if it's not there
        if not os.path.isdir(self.storage_dir):
            os.makedirs(self.storage_dir)

        # Try to create the log dir if it's not there
        if not os.path.isdir(self.log_dir):
            os.makedirs(self.log_dir)

        # additional helper attributes
        self.salt_root = os.path.join(self.storage_dir)
        self.salt_config_root = os.path.join(self.salt_root, 'salt')
        self.salt_master_config = os.path.join(self.salt_config_root, 'master')
        self.salt_cloud_config = os.path.join(self.salt_config_root, 'cloud')
        self.salt_core_states = os.path.join(self.storage_dir, 'core_states')
        self.salt_providers_dir = os.path.join(self.salt_config_root, 'cloud.providers.d')
        self.salt_profiles_dir = os.path.join(self.salt_config_root, 'cloud.profiles.d')

        if '{salt_version}' not in self.salt_bootstrap_args:
            raise ImproperlyConfigured('salt_bootstrap_args must contain `{salt_version}`')

        # defaults
        if not self.salt_master_log_level:  # pylint: disable=access-member-before-definition
            self.salt_master_log_level = 'info'

    def __getattr__(self, k):
        return self.get(k)

    def __setattr__(self, k, v):
        self[k] = v
