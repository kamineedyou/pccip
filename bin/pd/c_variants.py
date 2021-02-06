from enum import Enum
from typing import Set, Tuple
from pm4py.objects.log.log import EventLog
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.algo.discovery.causal import algorithm as causal_discovery
from pm4py.algo.discovery.causal.variants import alpha, heuristic


def alpha_causal_structure(log: EventLog,
                           params: dict = {}) -> Set[Tuple[str, str]]:
    """Get causal structure based of the alpha causal discovery.

    Args:
        log (EventLog): Event log to create a causal structure from.
        params (dict, optional): Parameters for the causal discovery algorithm.
                                 Defaults to {}.

    Returns:
        Set[Tuple[str, str]]: Sequence edges from the entire event log.
    """
    dfg = dfg_discovery.apply(log)
    return set(causal_discovery.apply(dfg, alpha).keys())


def heuristic_causal_structure(log: EventLog,
                               params: dict = {}) -> Set[Tuple[str, str]]:
    """Get causal structure based off of the heuristic causal discovery.

    Args:
        log (EventLog): Event log to create a causal structure from.
        params (dict, optional): Parameters for the causal discovery algorithm.
                                 Defaults to {}.

    Returns:
        Set[Tuple[str, str]]: Sequence edges from the entire event log.
    """

    # if parameters don't include threshold value, use a default value
    if 'threshold' not in params.keys():
        params['threshold'] = 0.5

    dfg = dfg_discovery.apply(log)
    sequence = causal_discovery.apply(dfg, heuristic)
    return {k for k, v in sequence.items() if v >= params['threshold']}


class Variants(Enum):
    """Causal structure discovery variant (c_algo) enum object.
    """
    DEFAULT_VARIANT = alpha_causal_structure
    ALPHA = alpha_causal_structure
    HEURISTIC = heuristic_causal_structure
