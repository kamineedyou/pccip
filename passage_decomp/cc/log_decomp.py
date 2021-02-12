from pm4py.objects.log.util import basic_filter
from pm4py.objects.log.log import EventLog
from typing import List


def decompose_event_log(log: EventLog, events: List[str]) -> EventLog:
    concept_name = "concept:name"
    parameter = {basic_filter.Parameters.ATTRIBUTE_KEY: concept_name}
    parameter[basic_filter.Parameters.POSITIVE] = True
    decomposed_Log = basic_filter.filter_log_events_attr(
        log, events, parameter)

    return decomposed_Log
