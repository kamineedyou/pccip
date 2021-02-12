from pm4py.objects.petri.importer import importer as pnml_importer


class WrongPetriNetModelType(Exception):
    pass


def importPetriNet(modelPath: str) -> tuple:
    'This function can only import pnml petri nets'
    if ".pnml" not in modelPath:
        raise WrongPetriNetModelType(
            "Wrong Petri net type we only support pnml format sofar")
    (net, initial_marking, final_marking) = pnml_importer.apply(modelPath)
    return (net, initial_marking, final_marking)
