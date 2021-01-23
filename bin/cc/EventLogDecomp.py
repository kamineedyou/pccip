from pm4py.objects.log.importer.xes import importer as xes_importer
import os
from pm4py.objects.log.util import basic_filter
from pm4py.objects.log.log import  EventLog
import pm4py


def decompose_event_log(log , array_events) -> EventLog:
    tracefilter_log_pos = basic_filter.filter_log_events_attr(log,array_events,
                                parameters={basic_filter.Parameters.ATTRIBUTE_KEY: "concept:name",
                                basic_filter.Parameters.POSITIVE: True})

    return EventLog(tracefilter_log_pos)
