from enum import Enum
from typing import Tuple
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.log.log import EventLog
from pm4py.algo.discovery.alpha.algorithm import apply as alpha_algo
from pm4py.algo.discovery.inductive.algorithm import apply as im_algo


def alpha_fragments(sublog: EventLog,
                    parameters: dict = None) \
                        -> Tuple[PetriNet, Marking, Marking]:
    """Discover the net fragment using the alpha miner.

    Args:
        sublog (EventLog): Sublog to do process discovery on.
        parameters (dict, optional): Parameters for the discovery algorithm.

    Returns:
        Tuple[PetriNet, Marking, Marking]: Net fragment
    """
    if parameters is None:
        parameters = {}

    return alpha_algo(sublog, parameters=parameters)


def inductive_fragments(sublog: EventLog,
                        parameters: dict = None) \
                            -> Tuple[PetriNet, Marking, Marking]:
    """Discover the net fragment using the inductive miner.

    Args:
        sublog (EventLog): Sublog to do process discovery on.
        parameters (dict, optional): Parameters for the discovery algorithm.

    Returns:
        Tuple[PetriNet, Marking, Marking]: Net fragment
    """
    if parameters is None:
        parameters = {}

    return im_algo(sublog, parameters=parameters)


class Variants(Enum):
    """Process discovery variant (p_algo) enum object.
    """
    DEFAULT_VARIANT = alpha_fragments
    ALPHA = alpha_fragments
    INDUCTIVE = inductive_fragments
