from pccip.bin.passages.passage import Passage
from pm4py.objects.petri import utils
from typing import List, Tuple
from pm4py.objects.petri.petrinet import PetriNet, Marking


Fragment = Tuple[PetriNet, Marking, Marking]


def net_fragments(passages: List[Passage], model: PetriNet) -> List[Fragment]:
    net_fragments = list()

    for passage in passages:
        X, Y = passage.getXY()
        init_marking = Marking()
        final_marking = Marking()
        places = model.places

        places_new = set()
        arcs_new = set()
        trans_new = set()
        for place in places:
            for arc in place.out_arcs:
                if arc.target.label in Y:
                    places_new.add(place)
                    trans_new.add(arc.target)
                    arcs_new.add(arc)

            for arc in place.in_arcs:
                if arc.source.label in X:
                    places_new.add(place)
                    trans_new.add(arc.source)
                    arcs_new.add(arc)

        fragment_net = PetriNet("new_petri_net")
        for place_new in places_new:
            if place_new.name == "end":
                final_marking[place_new] = 1

            if place_new.name == "start":
                init_marking[place_new] = 1

            fragment_net.places.add(place_new)

        for trans in trans_new:
            fragment_net.transitions.add(trans)

        for arc in arcs_new:
            arcs_new.add(arc)
            utils.add_arc_from_to(arc.source, arc.target, fragment_net)

        perti_net = tuple([fragment_net, init_marking, final_marking])
        net_fragments.append(perti_net)

    return net_fragments
