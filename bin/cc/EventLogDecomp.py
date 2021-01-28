from pm4py.objects.log.importer.xes import importer as xes_importer
import os
from pm4py.objects.log.util import basic_filter
from pm4py.objects.log.log import  EventLog
import pm4py
from typing import List

##
from pm4py.objects.log.exporter.xes import exporter as xes_exporter



def decompose_event_log(log:EventLog  , List_events:List[List]) -> EventLog:
    filtered_log = basic_filter.filter_log_events_attr(log,List_events,
                                parameters={basic_filter.Parameters.ATTRIBUTE_KEY: "concept:name",
                                basic_filter.Parameters.POSITIVE: True})

    return filtered_log


log = xes_importer.apply('test_log.xes')
List_events = ["a","c","b"]
filtered_log = basic_filter.filter_log_events_attr(log,List_events,
                        parameters={basic_filter.Parameters.ATTRIBUTE_KEY: "concept:name",
                        basic_filter.Parameters.POSITIVE: True})
xes_exporter.apply(filtered_log, 'filtered_log_test.xes')
