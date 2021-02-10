from bin.cc.extendModel import extendModel
from bin.utils.transformSkeleton import petriNetIntoSkeleton
from bin.passages.min_passages import algorithm
from pm4py.objects.petri.petrinet import PetriNet, Marking
from bin.cc.net_fragments import net_fragments
from bin.cc.Adapted_Cost import adapted_cost_func, fragment_fitness
from pm4py.objects.log.log import EventLog


def passage_decompose_conformanceChecking(net: PetriNet,
                                          initMarking: Marking,
                                          finalMarking: Marking,
                                          log: EventLog) -> float:
    (extendedNet, extendedInitMarking, extendedFinalMarking) = extendModel(
        net, initMarking, finalMarking)
    skeletonGraph = petriNetIntoSkeleton(extendedNet)
    transitionsOfExtendedNet = extendedNet.transitions
    silentTransOfExtended = [
        silentTrans for silentTrans
        in transitionsOfExtendedNet if silentTrans.label is None]
    passages = algorithm(skeletonGraph, silentTransOfExtended)
    fragments = net_fragments(passages, net, initMarking, finalMarking)
    print("works")
    fragment_cost = adapted_cost_func(log, fragments)
    overall_fitness = fragment_fitness(fragment_cost)
    return overall_fitness
