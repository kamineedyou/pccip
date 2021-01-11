from pm4py.objects.log.log import EventLog
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.algo.discovery.causal import algorithm as causal_discovery
from pm4py.algo.discovery.causal.variants import heuristic
from pm4py.algo.discovery.footprints import algorithm as foot_discovery


def generateCausalStructure(log: EventLog, variants: str = 'alpha') -> dict:
    if not isinstance(log, EventLog):
        raise TypeError('Invalid Log Type')

    causal = None

    if variants == 'alpha':
        causal = foot_discovery.apply(log, variant=foot_discovery.
                                      Variants.ENTIRE_EVENT_LOG)
    elif variants == 'heuristic':
        dfg = dfg_discovery.apply(log)
        causal = causal_discovery.apply(dfg, heuristic)
    else:
        raise TypeError("Variant is not supported.")

    return causal
