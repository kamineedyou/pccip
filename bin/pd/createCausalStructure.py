from typing import Set, Tuple
from pm4py.objects.log.log import EventLog
from pccip.bin.pd.c_variants import Variants
from pccip.bin.algorithm.constants import ARTIFICIAL_START, ARTIFICIAL_END


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


def create_custom_causal_structure(edges: Set[Tuple[str, str]]) \
                                                    -> Set[Tuple[str, str]]:
    """Function to make sure that the starting transition is only
    ARTIFICIAL_START and that the ending transition is only ARTIFICIAL_END.

    Args:
        edges (Set[Tuple[str, str]]): Custom causal structure.

    Returns:
        Set[Tuple[str, str]]: Complete custom causal structure.
    """
    # remove all self loops to make sure to find all start/end activities
    no_loop_edges = {edge for edge in edges if not edge[0] == edge[1]}

    # get all start transitions
    start_t = {x[0] for x in no_loop_edges
               if x[0] not in {y[1] for y in no_loop_edges}}
    # get all end transitions
    end_t = {y[1] for y in no_loop_edges
             if y[1] not in {x[0] for x in no_loop_edges}}

    causal = edges
    # if more than 1 start transition or artificial start in start transitions
    if len(start_t) > 1 or ARTIFICIAL_START not in start_t:
        to_add = {(ARTIFICIAL_START, x) for x in start_t
                  if not x == ARTIFICIAL_START}
        causal = causal | to_add

    # if more than 1 end transition or artificial end in end transitions
    if len(end_t) > 1 or ARTIFICIAL_END not in end_t:
        to_add = {(x, ARTIFICIAL_END) for x in end_t
                  if not x == ARTIFICIAL_END}
        causal = causal | to_add

    return causal
