from passage_decomp.cc.extendModel import extendModel
from passage_decomp.utils.transformSkeleton import petriNetIntoSkeleton
from passage_decomp.passages.min_passages import algorithm
from pm4py.objects.petri.petrinet import PetriNet, Marking
from passage_decomp.cc.net_fragments import create_net_fragments
from passage_decomp.cc.Adapted_Cost import adapted_cost_func, fragment_fitness
from pm4py.objects.log.log import EventLog


def passage_decompose_conformanceChecking(net: PetriNet,
                                          initMarking: Marking,
                                          finalMarking: Marking,
                                          log: EventLog):
    (extendedNet, extendedInitMarking, extendedFinalMarking) = extendModel(
        net, initMarking, finalMarking)
    skeletonGraph = petriNetIntoSkeleton(extendedNet)
    transitionsOfExtendedNet = extendedNet.transitions
    silentTransOfExtended = [
        silentTrans for silentTrans
        in transitionsOfExtendedNet if silentTrans.label is None]
    passages = algorithm(skeletonGraph, silentTransOfExtended)
    fragments = create_net_fragments(passages)
    fragment_alignment = adapted_cost_func(log, fragments)[0]
    overall_fitness = fragment_fitness(fragment_alignment)
    return overall_fitness
