from typing import Tuple
from pm4py.objects.petri.importer import importer as pnml_importer
from pm4py.objects.petri.petrinet import PetriNet, Marking


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
