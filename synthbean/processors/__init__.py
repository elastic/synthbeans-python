# -*- coding: utf-8 -*-
# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from elasticapm.conf.constants import SPAN, TRANSACTION
from elasticapm.processors import for_events
import math
import logging
import pprint


@for_events(TRANSACTION)
def span_smoother(client, event):
    # TODO make this smoothing value configurable?
    orig_val = event['duration']
    smoothed = math.floor(event['duration']/1000) * 1000
    event['duration'] = smoothed
    logging.debug(
        f"Logging a transaction with duration: {smoothed}. (Original value: {orig_val})")
    logging.debug(pprint.pformat(event))
    return event
