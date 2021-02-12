from networkx import DiGraph
from pm4py.objects.petri.petrinet import PetriNet


def petri_to_skeleton(net: PetriNet) -> DiGraph:
    """Transform a given petrinet into a skeleton graph

    Args:
        net (PetriNet): Given net

    Returns:
        DiGraph: Skeleton
    """
    skeleton = DiGraph()
    for place in net.places:
        for arcIn in place.in_arcs:
            for arcOut in place.out_arcs:
                skeleton.add_edge(arcIn.source, arcOut.target)
    return skeleton
