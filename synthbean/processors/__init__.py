# -*- coding: utf-8 -*-
from elasticapm.conf.constants import SPAN, TRANSACTION
from elasticapm.processors import for_events
import math
import logging
import pprint
import datetime

@for_events(TRANSACTION)
def span_smoother(client, event):
    ## TODO make this smoothing value configurable?
    orig_val = event['duration']
    smoothed = math.floor(event['duration']/1000) * 1000
    event['duration'] = smoothed
    logging.debug(f"Logging a transaction with duration: {smoothed}. (Original value: {orig_val})")
    logging.debug(pprint.pformat(event))
    return event