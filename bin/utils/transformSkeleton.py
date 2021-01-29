from networkx import DiGraph
from pm4py.objects.petri.petrinet import PetriNet


def petriNetIntoSkeleton(net: PetriNet) -> DiGraph:
    skeleton = DiGraph()
    for place in net.places:
        for arcIn in place.in_arcs:
            for arcOut in place.out_arcs:
                skeleton.add_edge(arcIn.source, arcOut.target)
    print(skeleton.edges)
    print(net.transitions)
    return skeleton
