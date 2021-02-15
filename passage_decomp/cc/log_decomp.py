from pm4py.objects.log.util import basic_filter
from pm4py.objects.log.log import EventLog, Trace
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


def efficient_log_decomp(log: EventLog, passage_list: List[str]) -> EventLog:
    """Projects the list of activities into the eventlog.

    Args:
        log (EventLog): given eventlog
        events (List[str]): activites to project

    Returns:
        EventLog: Projected eventlog
    """
    sublogs = {}
    for i, passage in enumerate(passage_list):
        sublogs[i] = {'activities': set(passage.getTVis()), 'log': [None]*len(log)}
        for trace_index in range(len(log)):
            sublogs[i]['log'][trace_index] = Trace()

    # prepare sublogs
    for i, trace in enumerate(log):
        for event in trace:
            for p in sublogs:
                # if activitiy is contained in passage, append the event
                if event['concept:name'] in sublogs[p]['activities']:
                    sublogs[p]['log'][i].append(event)

    return sublogs
