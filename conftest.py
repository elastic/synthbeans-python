# -*- coding: utf-8 -*-

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
