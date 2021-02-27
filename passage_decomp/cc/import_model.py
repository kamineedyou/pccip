from typing import Tuple
from pccip.passage_decomp.algorithm.constants import ARTIFICIAL_START, ARTIFICIAL_END
from pm4py.objects.petri.importer import importer as pnml_importer
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.log.log import EventLog


class WrongPetriNetModelType(Exception):
    pass


def import_petri_net(modelPath: str) -> Tuple[PetriNet, Marking, Marking]:
    """This function imports a petri with a given path

    Args:
        modelPath (str): [description]

    Raises:
        WrongPetriNetModelType: Petri net has wrong type only pnml are supported

    Returns:
        Tuple(PetriNet, Marking, Marking): return net, init marking, final marking
    """
    if ".pnml" not in modelPath:
        raise WrongPetriNetModelType(
            "Wrong Petri net type we only support pnml format sofar")
    (net, initial_marking, final_marking) = pnml_importer.apply(modelPath)
    return (net, initial_marking, final_marking)


def fix_transition_conflict(net: PetriNet, log: EventLog) -> None:
    """If the log and petri net already have the artificial start and end
    activities in the model/log (eg. from using passage process discovery),
    convert user's artificial labels to keep the artificial start/end unique.
    This is an in-place operation.

    Args:
        net (PetriNet): User's input petri net.
        log (EventLog): User's input event log.
    """
    start_exists = False
    end_exists = False

    start_user = f'{ARTIFICIAL_START}_user'
    end_user = f'{ARTIFICIAL_END}_user'

    for transition in net.transitions:
        if transition.name == ARTIFICIAL_START:
            start_exists = True
            transition.label = start_user
            transition.name = start_user
        elif transition.name == ARTIFICIAL_END:
            end_exists = True
            transition.label = end_user
            transition.name = end_user

    if start_exists or end_exists:
        for trace in log:
            for event in trace:
                if event['concept:name'] == ARTIFICIAL_START:
                    event['concept:name'] = start_user
                elif event['concept:name'] == ARTIFICIAL_END:
                    event['concept:name'] = end_user
