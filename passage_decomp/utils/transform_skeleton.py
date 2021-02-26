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
    inserted_transitions = set()
    for place in net.places:
        for arcIn in place.in_arcs:
            for arcOut in place.out_arcs:
                skeleton.add_edge(arcIn.source, arcOut.target)
                inserted_transitions.add(arcIn.source.label)
                inserted_transitions.add(arcOut.target.label)

    # add all transitions that have no places attached to it
    # (floating transitions)
    for t in net.transitions:
        if t.label not in inserted_transitions:
            skeleton.add_edge(t, t)

    return skeleton
