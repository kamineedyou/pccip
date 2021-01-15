from pm4py.objects.log.log import EventLog
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.algo.discovery.causal import algorithm as causal_discovery
from pm4py.algo.discovery.causal.variants import heuristic
from pm4py.algo.discovery.footprints import algorithm as foot_discovery


class Causal_Struct():
    def __init__(self, successors: set, parallel: set):
        self.successors = successors
        self.predecessors = self.generate_predecessors(successors)
        self.parallel = parallel

    def generate_predecessors(self, successors) -> set:
        pred = set()
        for match in successors:
            pred.add(match[::-1])

        return pred

    def __eq__(self, obj) -> bool:
        return isinstance(obj, Causal_Struct) and \
            self.successors == obj.successors and \
            self.predecessors == obj.predecessors and \
            self.parallel == obj.parallel

    def __ne__(self, obj) -> bool:
        return not self == obj


def generateCausalStructure(log: EventLog,
                            variants: str = 'alpha') -> Causal_Struct:
    if not isinstance(log, EventLog):
        raise TypeError('Invalid Log Type')

    causal = None
    if variants == 'alpha':
        foot = foot_discovery.apply(log, variant=foot_discovery.
                                    Variants.ENTIRE_EVENT_LOG)

        successors = foot['sequence']
        parallel = foot['parallel']

        causal = Causal_Struct(successors, parallel)

    elif variants == 'heuristic':
        dfg = dfg_discovery.apply(log)
        sequence = causal_discovery.apply(dfg, heuristic)
        successors = {k for k, v in sequence.items() if v >= 0}

        causal = Causal_Struct(successors, set())
    else:
        raise TypeError("Variant is not supported.")

    return causal
