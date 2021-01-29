from networkx import DiGraph
from pm4py.objects.petri.petrinet import PetriNet
from bin.cc.importModel import importPetriNet


class UnlabeledTransitions(Exception):
    pass


def petriNetIntoSkeleton(net: PetriNet) -> DiGraph:
    print(net.transitions)
    # for transation in net.transitions:
    # if transation.label is None:
    # raise UnlabeledTransitions(
    #  "Petri is has silent transitions pls remove them before")
    skeleton = DiGraph()
    for place in net.places:
        for arcIn in place.in_arcs:
            for arcOut in place.out_arcs:
                skeleton.add_edge(arcIn.source, arcOut.target)
    print(skeleton.edges)
    print(net.transitions)
    return skeleton


(net, init, final) = importPetriNet("testModelPNML.pnml")

print(net.transitions)

petriNetIntoSkeleton(net)
