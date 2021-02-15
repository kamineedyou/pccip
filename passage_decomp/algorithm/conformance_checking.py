from pccip.passage_decomp.cc.extend_model import extend_model
from pccip.passage_decomp.utils.transform_skeleton import petri_to_skeleton
from pccip.passage_decomp.passages.min_passages import min_passages
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pccip.passage_decomp.cc.net_fragments import create_net_fragments
from pccip.passage_decomp.cc.adapted_cost import passage_alignment, get_global_fitness
from pm4py.objects.log.log import EventLog
from typing import Tuple


def passage_conformance_checking(log: EventLog,
                                 net: PetriNet,
                                 init_marking: Marking,
                                 final_marking: Marking) -> Tuple[dict, dict]:
    """Conformance checking decomposition with passages

    Args:
        log (EventLog): Event log to check the model with
        net (PetriNet): Input petri net to test the log against
        init_marking (Marking): Initial marking of the petri net
        final_marking (Marking): Final marking of the petri net

    Returns:
        Tuple[dict, dict]: local alignments and global fitness values
    """

    # extend the input model
    ext_net, ext_im, ext_fm = extend_model(net, init_marking, final_marking)

    # generate the skeleton
    skeleton = petri_to_skeleton(ext_net)

    # get all silent transition names in the petri net
    silent_names = {silent.name for silent in ext_net.transitions
                    if not silent.label}

    # generate all the minimal passages
    passages = min_passages(skeleton, silent_names)

    # decompose initial petri net into net fragments
    fragments = create_net_fragments(passages)

    # calculate local alignments for each net fragment
    local_align = passage_alignment(fragments, log)

    # calculate global statistics over all passages
    global_fitness = get_global_fitness(local_align, log,
                                        (net, init_marking, final_marking))

    return local_align, global_fitness
