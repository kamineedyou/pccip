from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.petri import utils
from typing import Tuple


class NoInitialMarking(Exception):
    pass


class NoFinalMarking(Exception):
    pass


def extendModel(net: PetriNet,
                initial_marking: Marking,
                final_marking: Marking) -> Tuple[PetriNet, Marking, Marking]:
    "Returnds the extended petrinet Model"
    if not initial_marking:
        raise NoInitialMarking("No initial marking defined")

    if not final_marking:
        raise NoFinalMarking("No final marking defined")

    t_bot = PetriNet.Transition("BOT", "BOT")
    t_top = PetriNet.Transition("TOP", "TOP")
    net.transitions.add(t_bot)
    net.transitions.add(t_top)
    for currentSource in initial_marking:
        utils.add_arc_from_to(t_top, currentSource, net)

    for currentSink in final_marking:
        utils.add_arc_from_to(currentSink, t_bot, net)

    return (net, initial_marking, final_marking)
