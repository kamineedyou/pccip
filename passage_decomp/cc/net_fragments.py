from pm4py.objects.petri.petrinet import PetriNet, Marking
from passage_decomp.passages.passage import Passage
from passage_decomp.algorithm.constants import ARTIFICIAL_START, ARTIFICIAL_END
from typing import Set, List, Tuple
from copy import deepcopy


def create_net_fragments(passages: Set[Passage]) -> List[PetriNet]:
    net_fragments = []

    for p in passages:
        border_x = p.getBorderX()
        border_y = p.getBorderY()
        new_net = PetriNet(name=str(border_x))
        # iterate through all passage edges.
        # Each Transition only gets processed once.
        for edge in p.edges:
            edge_dict = p.get_digraph_edge(edge)
            for tran in edge_dict:
                if tran not in new_net.transitions:

                    if tran.name not in border_x:
                        for arc in tran.in_arcs:
                            new_net.places.add(arc.source)
                            new_net.transitions.add(arc.target)
                            new_net.arcs.add(arc)

                    if tran.name not in border_y:
                        for arc in tran.out_arcs:
                            new_net.places.add(arc.target)
                            new_net.transitions.add(arc.source)
                            new_net.arcs.add(arc)

        net_fragments.append((deepcopy(new_net), p))

    return clean_fragments(net_fragments)


def clean_fragments(net_fragments: List[Tuple[PetriNet, Passage]]) \
        -> List[Tuple[PetriNet, Marking, Marking]]:
    final_fragments = []

    for net, p in net_fragments:
        border_x = p.getBorderX()
        border_y = p.getBorderY()

        for tran in net.transitions:
            if tran.name in border_x and tran.name != ARTIFICIAL_START:
                tran.in_arcs.clear()
            elif tran.name in border_y and tran.name != ARTIFICIAL_END:
                tran.out_arcs.clear()

        im_tran = {tran for tran in net.transitions
                   if tran.name == ARTIFICIAL_START}
        fm_tran = {tran for tran in net.transitions
                   if tran.name == ARTIFICIAL_END}

        if im_tran:
            im_dict = {}
            for arc in next(iter(im_tran)).out_arcs:
                im_dict[arc.target] = 1

            im = Marking(im_dict)
        else:
            im = Marking()

        if fm_tran:
            fm_dict = {}
            for arc in next(iter(fm_tran)).in_arcs:
                fm_dict[arc.source] = 1

            fm = Marking(fm_dict)
        else:
            fm = Marking()

        final_fragments.append((net, im, fm))

    return final_fragments
