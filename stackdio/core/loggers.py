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

from stackdio.core.channel import StackdioGroup


class WebSocketHandler(logging.Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a websocket.
    """

    def __init__(self, stack_id, log_type):
        """
        Initialize the handler.
        """
        logging.Handler.__init__(self)
        self.group = StackdioGroup('/stacks/{}/logs/{}/'.format(stack_id, log_type))

    def emit(self, record):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the websocket.
        """
        try:
            msg = self.format(record)
            self.group.send({
                'log_msg': msg
            })
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)
            raise
