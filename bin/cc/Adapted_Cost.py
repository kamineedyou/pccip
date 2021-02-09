from pm4py.algo.conformance.decomp_alignments.variants import recompos_maximal
from pm4py.objects.log.log import EventLog
from pm4py.objects.petri.petrinet import PetriNet, Marking
from typing import Tuple, List, Set
# Get the misaligned activity from the alignment tuple


def get_acti(activity: Tuple[str, str]) -> str:
    """
    retrieve activities where misalignment occured.

    Parameters
    ----------
    activity : Tuple[str, str]

    Returns
    -------
    str: misaligned activity

    """
    SKIP = '>>'
    if activity is not None and SKIP in activity:
        if activity[0] != SKIP:
            return activity[0]
        else:
            return activity[1]


def get_misaligned_trans(aligned_traces: List) -> List[Set[str]]:
    """Get all the misaligned transitions So that later we can
        check whether they are in other net fragments.

    Parameters
    ----------
    aligned_traces : List contains the alignments
     (ie: after performing alignment)

    Returns
    -------
    List[Set[str]]: misaligned activities for each trace

    """
    lis = list()
    for trace in aligned_traces:
        unfited_traces = set()
        if trace['cost'] != 0:
            for alig in trace['alignment']:
                if get_acti(alig) is not None \
                                  and get_acti(alig) not in unfited_traces:
                    unfited_traces.add(get_acti(alig))
        if unfited_traces not in lis:
            lis.append(unfited_traces)
    return lis


def adapted_cost_func(log: EventLog,
                      net_fragments: List[Tuple[PetriNet,
                                                Marking,
                                                Marking]]) -> List[dict]:
    """performing an alignment on top of each net fragment.

    Parameters
    ----------
    log : EventLog
    net_fragments : List[Tuple[PetriNet,Marking,Marking]]

    Returns
    -------
    List[dict]
        list where each dictionary contains alignment information of the
         corresponding net fragment.

    """

    misaligned_trans = {}
    aligned_traces = {}
    total_cost = {}
    for frag in net_fragments:
        frag[0].lvis_labels = [str(acti.label) for acti in
                               frag[0].transitions if acti.label]
    for i, fragment in enumerate(net_fragments):
        aligned_traces[i] = recompos_maximal.apply_log(log, [fragment])
        misaligned_trans[i] = get_misaligned_trans(aligned_traces[i])
        for trace in range(len(misaligned_trans[i])):
            total = 0
            count_trace = 0
            for j in range(len(net_fragments)):
                count_trace = len(
                    set(misaligned_trans[i][trace]).
                    intersection(net_fragments[j][0].lvis_labels)) * 10000

            if count_trace != 0:
                aligned_traces[i][trace]['cost'] /= count_trace

            total += aligned_traces[i][trace]['cost']

        total_cost[i] = total

    return aligned_traces, total_cost
