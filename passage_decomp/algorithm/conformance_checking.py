from pccip.passage_decomp.cc.extend_model import extend_model
from pccip.passage_decomp.utils.transform_skeleton import petri_to_skeleton
from pccip.passage_decomp.passages.min_passages import algorithm
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pccip.passage_decomp.cc.net_fragments import create_net_fragments
from pccip.passage_decomp.cc.adapted_cost import adapted_cost_func, fragment_fitness
from pm4py.objects.log.log import EventLog


def passage_conformance_checking(net: PetriNet,
                                 init_marking: Marking,
                                 final_marking: Marking,
                                 log: EventLog):

    # extend the input model
    ext_net, ext_im, ext_fm = extend_model(net, init_marking, final_marking)

    # generate the skeleton
    skeletonGraph = petri_to_skeleton(ext_net)

    # get all silent transition names in the petri net
    silent_names = [silent.name for silent in ext_net.transitions
                    if not silent.label]

    # generate all the minimal passages
    passages = algorithm(skeletonGraph, silent_names)

    # decompose initial petri net into net fragments
    fragments = create_net_fragments(passages)

    # perform alignment cost check with the input log on the fragments
    fragment_alignment = adapted_cost_func(log, fragments)[0]

    # generate return value
    overall_fitness = fragment_fitness(fragment_alignment)

    return overall_fitness
