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

import logging

from channels.auth import channel_session_user_from_http, channel_session_user
from channels.channel import Group

logger = logging.getLogger(__name__)


@channel_session_user_from_http
def ws_connect(message):
    # Just add it to the group
    Group(message['path']).add(message.reply_channel)
    # Save the path
    message.channel_session['path'] = message['path']


@channel_session_user
def ws_disconnect(message):
    # Just remove it from the group
    Group(message.channel_session['path']).discard(message.reply_channel)
