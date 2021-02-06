from enum import Enum
from pm4py.objects.petri.petrinet import PetriNet
from pm4py.objects.log.log import EventLog
from pm4py.algo.discovery.alpha.algorithm import apply as alpha_algo
from pm4py.algo.discovery.inductive.algorithm import apply as im_algo


def alpha_fragments(sublog: EventLog, parameters: dict = None) -> PetriNet:
    if parameters is None:
        parameters = {}

    return alpha_algo(sublog, parameters=parameters)


def inductive_fragments(sublog: EventLog, parameters: dict = None) -> PetriNet:
    if parameters is None:
        parameters = {}

    return im_algo(sublog, parameters=parameters)


class Variants(Enum):
    DEFAULT_VARIANT = alpha_fragments
    ALPHA = alpha_fragments
    INDUCTIVE = inductive_fragments
