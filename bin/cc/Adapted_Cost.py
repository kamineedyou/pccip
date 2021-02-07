from pm4py.algo.conformance.alignments import algorithm as alignments
from pm4py.evaluation.replay_fitness import evaluator as replay_fitness
from pm4py.objects.log.log import EventLog
from pm4py.objects.petri.petrinet import PetriNet, Marking
from typing import Tuple, List, Set
# Get the misaligned activity from the alignment tuple


def get_acti(activity: Tuple[str, str]) -> str:
    SKIP = '>>'
    if x is not None and SKIP in x:
        if activity[0] != SKIP:
            return activity[0]
        else:
            return activity[1]


# Get all the misaligned transitions and store them in a "lis"
#so that later we can check whether they are in other net fragments
def get_misaligned_trans(aligned_traces: List) -> List[Set[str]]:
    lis = list[]
    for trace in aligned_traces:
        unfited_traces = set()
        if trace['fitness'] != 1:
            for alig in trace['alignment']:
                if get_Acti(alig) is not None \
                                  and get_Acti(alig) not in unfited_traces:
                    unfited_traces.add(get_Acti(alig))
        lis.append(unfited_traces)
    return lis


def discover_final_marking(petri):

    final_marking = Marking()

    for place in petri.places:
        if len(place.out_arcs) == 0:
            final_marking[place] = 1

    return final_marking


def discover_initial_marking(petri):

    initial_marking = Marking()

    for place in petri.places:
        if len(place.in_arcs) == 0:
            initial_marking[place] = 1

    return initial_marking


def adapted_cost_func(subevents: List[EventLog],
                      net_fragments: List[PetriNet]) -> List[dict]:
    misaligned_trans = {}
    aligned_traces = {}
    average_fitness = {}
    for fragment in net_fragments:
        initial_marking = discover_initial_marking(fragment)
        final_marking = discover_final_marking(fragment)
        for i in range(len(subevents)):
            aligned_traces[i] = alignments.apply_log(subevents[i],
                                                     fragment,
                                                     initial_marking,
                                                     final_marking)
            misaligned_trans[i] = get_misaligned_trans(aligned_traces[i])
            for trace in range(len(misaligned_trans[i])):
                count_trace = 0
                for j in range(len(net_fragments)):
                    if (k in set(misaligned_trans[i][trace]) for
                            k in str(net_fragments[j].transitions)):
                        count_trace += 10000
                if count_trace != 0:
                    aligned_traces[i][trace]['cost'] /= count_trace
            average_fitness[i] = replay_fitness.evaluate(
                        aligned_traces[i],
                        variant=replay_fitness.Variants.ALIGNMENT_BASED)
    return aligned_traces, average_fitness
