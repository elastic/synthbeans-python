# -*- coding: utf-8 -*-
import synthbean.processors

def test_span_smoother(non_normalized_event_fixture, normalized_event_fixture):
    """
    GIVEN a transaction
    WHEN the event is passed through the span smoother
    THEN smoothed values are returned in the event
    """
    got = synthbean.processors.span_smoother(None, non_normalized_event_fixture)
    want = normalized_event_fixture
    assert got == want

