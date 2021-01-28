from pm4py.objects.log.util import basic_filter
from pm4py.objects.log.log import EventLog
from typing import List


def decompose_event_log(log: EventLog, List_events: List[List]) -> EventLog:
    parameters = {basic_filter.Parameters.ATTRIBUTE_KEY: "concept:name", basic_filter.Parameters.POSITIVE: True}
    filtered_log = basic_filter.filter_log_events_attr(log, List_events, parameters)

    return filtered_log
