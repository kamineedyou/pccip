from enum import Enum
from typing import Set, Tuple
from pm4py.objects.log.log import EventLog
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.algo.discovery.causal import algorithm as causal_discovery
from pm4py.algo.discovery.causal.variants import heuristic
from pm4py.algo.discovery.footprints import algorithm as a_discovery


def alpha_causal_structure(log: EventLog,
                           params: dict = {}) -> Set[Tuple[str, str]]:
    foot = a_discovery.apply(log,
                             variant=a_discovery.Variants.ENTIRE_EVENT_LOG)
    return foot['sequence']


def heuristic_causal_structure(log: EventLog,
                               params: dict = {}) -> Set[Tuple[str, str]]:

    # if parameters don't include threshold value, use a default value
    if 'threshold' not in params.keys():
        params['threshold'] = 0.5

    dfg = dfg_discovery.apply(log)
    sequence = causal_discovery.apply(dfg, heuristic)
    return {k for k, v in sequence.items() if v >= params['threshold']}


class Variants(Enum):
    DEFAULT_VARIANT = alpha_causal_structure
    ALPHA = alpha_causal_structure
    HEURISTIC = heuristic_causal_structure
