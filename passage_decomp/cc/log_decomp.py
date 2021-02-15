from pm4py.objects.log.util import basic_filter
from pm4py.objects.log.log import EventLog, Trace
from pccip.passage_decomp.passages.passage import Passage
from typing import Set


def decompose_event_log(log: EventLog, events: Set[str]) -> EventLog:
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
        log, list(events), parameter)

    return decomposed_Log


def efficient_log_decomp(log: EventLog, passage_set: Set[Passage]) -> EventLog:
    """Projects the list of activities into the eventlog.

    Args:
        log (EventLog): given eventlog
        passage_set (List[Passage]): passages connected to the log

    Returns:
        EventLog: Projected eventlog
    """
    sublogs = {}
    for i, passage in enumerate(passage_set):
        sublogs[i] = {'activities': passage.getTVis(), 'log': [None]*len(log)}
        for trace_index in range(len(log)):
            sublogs[i]['log'][trace_index] = Trace()

    # prepare sublogs
    for i, trace in enumerate(log):
        for event in trace:
            for p in sublogs:
                # if activitiy is contained in passage, append the event
                if event['concept:name'] in sublogs[p]['activities']:
                    sublogs[p]['log'][i].append(event)

    event_logs = []
    for sublog_index in sublogs:
        event_log = EventLog()
        for trace in sublogs[sublog_index]['log']:
            event_log.append(trace)
        event_logs.append(event_log)

    return event_logs
