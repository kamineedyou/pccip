from bin.passages.passage import Passage
from pm4py.objects.petri import utils
from typing import List
from pm4py.objects.petri.petrinet import PetriNet, Marking
import re
import copy


def net_fragments(passages: List[Passage], model: PetriNet,
                  im: Marking, fm: Marking) -> List[PetriNet]:
    net_fragments = list()
    init_marking_name = re.findall(r"'(.*?):", str(im))
    final_markin_name = re.findall(r"'(.*?):", str(fm))
    for passage in passages:
        x, y = passage.getXY()
        init_marking = Marking()
        final_marking = Marking()
        places = model.places

        fragment_net = PetriNet("new_petri_net")
        for place in places:
            place_new = copy.deepcopy(place)

            for arc in place.out_arcs:
                if arc.target.label in y:
                    fragment_net.places.add(place_new)
                    trans_new = copy.deepcopy(arc.target)
                    fragment_net.transitions.add(trans_new)
                    utils.add_arc_from_to(place_new, trans_new, fragment_net)
                    if str(place_new.name) == init_marking_name[0]:
                        init_marking[place_new] = 1
                        fragment_net.places.add(place_new)

            for arc in place.in_arcs:
                if arc.source.label in x:
                    fragment_net.places.add(place_new)
                    trans_new = copy.deepcopy(arc.source)
                    fragment_net.transitions.add(trans_new)
                    utils.add_arc_from_to(trans_new, place_new, fragment_net)
                    if str(place_new.name) == final_markin_name[0]:
                        final_marking[place_new] = 1
                        fragment_net.places.add(place_new)

        net_fragments.append((fragment_net, init_marking, final_marking))

    return net_fragments
