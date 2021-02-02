from pccip.bin.passages.passage import Passage
from pm4py.objects.petri import utils
from typing import List
from pm4py.objects.petri.petrinet import PetriNet


def net_fragments(passage_list: List[Passage], process_model: PetriNet) -> List[PetriNet]:
    NnetFragments = list()

    for passage in passage_list:
        X, Y = passage.getXY()

        places = process_model.places

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
            fragment_net.places.add(place_new)
        for trans in trans_new:
            fragment_net.transitions.add(trans)

        for arc in arcs_new:
            arcs_new.add(arc)
            utils.add_arc_from_to(arc.source, arc.target, fragment_net)

        NnetFragments.append(fragment_net)

    return NnetFragments
