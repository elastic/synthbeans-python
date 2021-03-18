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

from pytest import fixture

@fixture
def non_normalized_event_fixture():
    event = {
        'context': {'tags': {}},
        # This is non-normalized so we use a raw value
        # for the duration
        'duration': 1001,
        'id': '52c61fd7afa74799',
        'name': 'first_span',
        'outcome': None,
        'result': 'success',
        'sample_rate': 1.0,
        'sampled': True,
        'span_count': {'dropped': 0, 'started': 0},
        'timestamp': 1615820260235384,
        'trace_id': '73844e424d8fae7746d980f72eaf87cf',
        'type': 'script'}
    return event

@fixture
def normalized_event_fixture():
    event = {
        'context': {'tags': {}},
        # This is normalized
        'duration': 1000,
        'id': '52c61fd7afa74799',
        'name': 'first_span',
        'outcome': None,
        'result': 'success',
        'sample_rate': 1.0,
        'sampled': True,
        'span_count': {'dropped': 0, 'started': 0},
        'timestamp': 1615820260235384,
        'trace_id': '73844e424d8fae7746d980f72eaf87cf',
        'type': 'script'}
    return event
