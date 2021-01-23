from networkx import DiGraph
from pm4py.objects.petri.petrinet import PetriNet


class UnlabeledTransitions(Exception):
    pass


def petriNetIntoSkeleton(net: PetriNet) -> DiGraph:
    for transation in net.transitions:
        if transation.label is None:
            raise UnlabeledTransitions(
                "Petri has silent transitions pls remove them before")
    skeleton = DiGraph()
    for place in net.places:
        for arcIn in place.in_arcs:
            for arcOut in place.out_arcs:
                skeleton.add_edge(arcIn.source, arcOut.target)
    return skeleton
