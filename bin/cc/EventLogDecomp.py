from pm4py.objects.log.util import basic_filter
from pm4py.objects.log.log import EventLog
from typing import List


def decompose_event_log(log: EventLog, List_events: List[str]) -> EventLog:
    c_name = "concept:name"
    par = {basic_filter.Parameters.ATTRIBUTE_KEY: c_name}
    par[basic_filter.Parameters.POSITIVE] = True
    filtered_log = basic_filter.filter_log_events_attr(log, List_events, par)

    return filtered_log
