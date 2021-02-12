from pm4py.objects.log.util import basic_filter
from pm4py.objects.log.log import EventLog
from typing import List


def decompose_event_log(log: EventLog, events: List[str]) -> EventLog:
    """Projects the list of activities into the eventlog.

    Args:
        log (EventLog): given eventlog
        events (List[str]): activites to project

    Returns:
        EventLog: Projected eventlog
    """
    concept_name = "concept:name"
    parameter = {basic_filter.Parameters.ATTRIBUTE_KEY: concept_name}
    parameter[basic_filter.Parameters.POSITIVE] = True
    decomposed_Log = basic_filter.filter_log_events_attr(
        log, events, parameter)

    return decomposed_Log
