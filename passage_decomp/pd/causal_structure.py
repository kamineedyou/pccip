from typing import Set, Tuple
from pm4py.objects.log.log import EventLog
from pm4py.statistics.start_activities.log.get import get_start_activities
from pm4py.statistics.end_activities.log.get import get_end_activities
from pccip.passage_decomp.pd.c_variants import Variants
from pccip.passage_decomp.algorithm.constants import ARTIFICIAL_START, ARTIFICIAL_END
from pccip.passage_decomp.cc.EventLogDecomp import decompose_event_log


def create_causal_structure(log: EventLog,
                            variant: str = 'DEFAULT_VARIANT',
                            params: dict = None) -> Set[Tuple[str, str]]:
    """Generate the causal structure (sequence edges) from an event log.

    Args:
        log (EventLog): Event log to create a causal structure from.
        variant (str, optional): Causal algorithm variant to create a
                                 causal structure.
                                 Variants available: 'ALPHA', 'HEURISTIC'.
                                 Defaults to 'DEFAULT_VARIANT'.
        params (dict, optional): Parameters for the discovery algorithm.
                                 Defaults to None.

    Raises:
        TypeError: Raised when input is not of type EventLog.
        TypeError: Raised when the variant is invalid.

    Returns:
        Set[Tuple[str, str]]: Sequence edges from the entire event log.
    """
    if not isinstance(log, EventLog):
        raise TypeError('Invalid Log Type')

    variant = getattr(Variants, variant.upper(), None)
    if variant is None:
        raise TypeError('Invalid input variant (c_algo)')

    if params is None:
        params = {}

    return variant(log, params)


def create_custom_causal_structure(edges: Set[Tuple[str, str]], xes: EventLog)\
        -> Set[Tuple[str, str]]:
    """Function to make sure that the starting transition is only
    ARTIFICIAL_START and that the ending transition is only ARTIFICIAL_END.

    Args:
        edges (Set[Tuple[str, str]]): Custom causal structure.
        xes (EventLog): Event Log to be used by algorithm.

    Returns:
        Set[Tuple[str, str]]: Complete custom causal structure.
    """
    visible_activities = list({act for tup in edges for act in tup}
                              - {ARTIFICIAL_START, ARTIFICIAL_END})
    filtered_log = decompose_event_log(xes, visible_activities)

    # get all start transitions
    start_t = {k for k in get_start_activities(filtered_log).keys()}
    # get all end transitions
    end_t = {k for k in get_end_activities(filtered_log).keys()}

    # if more than 1 start transition or artificial start in start transitions
    # and if more than 1 end transition or artificial end in end transitions
    causal = edges | \
        {(ARTIFICIAL_START, x) for x in start_t} | \
        {(x, ARTIFICIAL_END) for x in end_t}

    return causal
