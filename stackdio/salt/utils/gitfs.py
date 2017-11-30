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

from __future__ import absolute_import, print_function, unicode_literals

import io
import logging
import os
from shutil import rmtree

import git
import salt.config
import salt.fileserver
import salt.payload
import salt.utils
import salt.utils.event
from salt.utils.gitfs import (
    GitFS,
    GitPython,
)

PER_REMOTE_OVERRIDES = ('base', 'mountpoint', 'root', 'ssl_verify', 'privkey')

_INVALID_REPO = (
    'Cache path {0} (corresponding remote: {1}) exists but is not a valid '
    'git repository. You will need to manually delete this directory on the '
    'master to continue to use this {2} remote.'
)

logger = logging.getLogger(__name__)


class StackdioGitPython(GitPython):

    def __init__(self, *args, **kwargs):
        super(StackdioGitPython, self).__init__(*args, **kwargs)
        # Set these lists
        self.env_whitelist = None
        self.env_blacklist = None

    def _get_remote_env(self):
        remote_env = {}

        private_key_file = getattr(self, 'privkey', None)

        if private_key_file:
            git_wrapper = salt.utils.path_join(self.cache_root, '{}.sh'.format(self.hash))
            with io.open(git_wrapper, 'w') as f:
                f.write('#!/bin/bash\n')
                f.write('SSH=$(which ssh)\n')
                f.write('exec $SSH -o StrictHostKeyChecking=no -i {} "$@"\n'.format(
                    private_key_file
                ))

            # Make the git wrapper executable
            os.chmod(git_wrapper, 0o755)

            remote_env['GIT_SSH'] = git_wrapper

        return remote_env

    def init_remote(self):
        """
        Same as GitPython:init_remote(), we just do the call to update_environment after
        creating the repo.
        """
        new = False
        if not os.listdir(self.cachedir):
            # Repo cachedir is empty, initialize a new repo there
            self.repo = git.Repo.init(self.cachedir)
            self.repo.git.update_environment(**self._get_remote_env())
            new = True
        else:
            # Repo cachedir exists, try to attach
            try:
                self.repo = git.Repo(self.cachedir)
                self.repo.git.update_environment(**self._get_remote_env())
            except git.exc.InvalidGitRepositoryError:
                logger.error(_INVALID_REPO.format(self.cachedir, self.url, self.role))
                return new

        self.gitdir = salt.utils.path_join(self.repo.working_dir, '.git')

        if not self.repo.remotes:
            try:
                self.repo.create_remote('origin', self.url)
            except os.error:
                # This exception occurs when two processes are trying to write
                # to the git config at once, go ahead and pass over it since
                # this is the only write. This should place a lock down.
                pass
            else:
                new = True

            try:
                ssl_verify = self.repo.git.config('--get', 'http.sslVerify')
            except git.exc.GitCommandError:
                ssl_verify = ''
            desired_ssl_verify = str(self.ssl_verify).lower()
            if ssl_verify != desired_ssl_verify:
                self.repo.git.config('http.sslVerify', desired_ssl_verify)

            # Ensure that refspecs for the "origin" remote are set up as configured
            if hasattr(self, 'refspecs'):
                self.configure_refspecs()

        return new


class StackdioGitFS(GitFS):

    def get_provider(self):
        """
        Always use the StackdioGitPython provider
        """
        self.provider = 'stackdiogitpython'
        self.provider_class = StackdioGitPython

    # Make it work as a contextmanager
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.opts.get('cleanup_cachedir', False):
            if os.path.isdir(self.opts['cachedir']):
                logger.debug('Cleaning up gitfs cachedir: {}'.format(self.opts['cachedir']))
                rmtree(self.opts['cachedir'])
        return False
