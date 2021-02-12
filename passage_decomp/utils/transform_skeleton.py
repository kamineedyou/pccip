from networkx import DiGraph
from pm4py.objects.petri.petrinet import PetriNet


def petri_to_skeleton(net: PetriNet) -> DiGraph:
    skeleton = DiGraph()
    for place in net.places:
        for arcIn in place.in_arcs:
            for arcOut in place.out_arcs:
                skeleton.add_edge(arcIn.source, arcOut.target)
    return skeleton
