from typing import Tuple, List
from pm4py.objects.log.log import EventLog, Trace
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.algo.conformance.alignments.variants.dijkstra_less_memory import get_best_worst_cost
from pm4py.algo.conformance.alignments.algorithm import apply_trace, VERSION_DIJKSTRA_NO_HEURISTICS


def passage_alignment(fragments: List[Tuple[PetriNet, Marking, Marking]],
                      log: EventLog) -> dict:
    """Calculate the local passage alignments for all of the input net
    fragments that were calculated using passages.

    Args:
        fragments (List[Tuple[PetriNet, Marking, Marking]]): input net
            fragments generated from passages.
        log (EventLog): whole event log to test the net fragments against.

    Returns:
        dict: Dictionary containing alignment results for each fragment
            keys:
                petri: PetriNet, Marking, Marking of the fragment.
                unfit_traces: all ids of traces that are non-fitting to the
                    fragment.
                costs: local alignment costs (transition specific).
                sublog: sublog traces used on the fragment.
                local_align: local alignments of the sublog on the fragment.
    """
    # prepare local alignment object
    local_alignment = {}
    remove_empty_traces(log)
    for i, fragment in enumerate(fragments):
        local_alignment[i] = {}
        local_alignment[i]['unfit_traces'] = set()
        local_alignment[i]['petri'] = (fragment[0], fragment[1], fragment[2])
        local_alignment[i]['costs'] = {}
        # initialize all costs to 0
        for t_vis in [t.label for t in fragment[0].transitions if t.label]:
            local_alignment[i]['costs'][t_vis] = 0.0

        # initialize empty traces
        local_alignment[i]['sublog'] = [None]*len(log)
        for trace_index in range(len(log)):
            local_alignment[i]['sublog'][trace_index] = Trace()

    # count how many times each transition appears in the fragments
    transition_trace_counter = count_transition_trace(local_alignment)

    # prepare sublogs
    for i, trace in enumerate(log):
        for event in trace:
            for f in local_alignment:
                # if activitiy is contained in passage, append the event
                if event['concept:name'] in local_alignment[f]['costs']:
                    local_alignment[f]['sublog'][i].append(event)

    # compute the local alignments
    for f in local_alignment:
        trace_summary = count_trace_occurances(local_alignment[f])
        get_alignment(trace_summary, local_alignment[f]['petri'])

        # count how many errors there was of each transition in the passage
        count_transition_errors(trace_summary)

        # project the summary onto local alignment object
        unwrap_alignment(local_alignment[f], trace_summary)

        # adapt the cost to account for multiple of same label in
        # other fragments
        adapted_cost(local_alignment[f], transition_trace_counter)

    return local_alignment


def count_transition_trace(alignment_obj: dict) -> dict:
    """Counts in how many passages a each transition exists.

    Args:
        alignment_obj (dict): local alignment dictionary

    Returns:
        dict: Dictionary with transition label as key and number of passages
            the transition is in as value.
    """
    transition_counter = {}
    for f in alignment_obj:
        t_vis = alignment_obj[f]['costs'].keys()
        for transition in t_vis:
            if transition in transition_counter.keys():
                transition_counter[transition] += 1
            else:
                transition_counter[transition] = 1

    return transition_counter


def unwrap_alignment(alignment_obj, trace_summary):
    """Unwrap the summary back into alignments for every trace in the sublog.

    Args:
        alignment_obj (dict): Local alignment dictionary.
        trace_summary (dict): Trace summary containing one of each trace type.
    """
    trace_align = [None]*len(alignment_obj['sublog'])
    total_costs = {}
    total_unfit = set()
    for i, trace in enumerate(alignment_obj['sublog']):
        trace_id = ''.join([e['concept:name'] for e in trace])
        trace_align[i] = trace_summary[trace_id]['alignment']

        if not total_costs:
            total_costs = trace_summary[trace_id]['cost']
        if not trace_summary[trace_id]['fit']:
            total_unfit.add(i)

    alignment_obj['local_align'] = trace_align
    alignment_obj['unfit_traces'] = total_unfit
    alignment_obj['costs'] = total_costs


def count_trace_occurances(alignment_obj):
    """Count the trace occurances in the sublog. This is done such that the
    alignment function only has to find the optimal alignments for a given
    trace once and can use the same value for each of the sublogs.

    Args:
        alignment_obj (dict): Local alignment dictionary.

    Returns:
        dict: Trace summary containing one of each trace type.
    """
    trace_list = {}
    for trace in alignment_obj['sublog']:
        trace_id = ''.join([e['concept:name'] for e in trace])
        if trace_id not in trace_list:
            trace_list[trace_id] = {}
            trace_list[trace_id]['trace'] = trace
            trace_list[trace_id]['count'] = 1
            trace_list[trace_id]['cost'] = alignment_obj['costs']
            trace_list[trace_id]['fit'] = True
        else:
            trace_list[trace_id]['count'] += 1

    return trace_list


def adapted_cost(alignment_obj: dict, global_t_count: dict) -> None:
    """In place function that adapts the total cost of all local alignment
    costs from each passage to account for multiple passages containing the
    same transition.

    Args:
        alignment_obj (dict): local alignment dictionary
        global_t_count (dict): dictionary containing how many times each
            transition exists in the set of passages
    """
    for transition in alignment_obj['costs']:
        if global_t_count[transition] > 1:
            alignment_obj['costs'][transition] /= global_t_count[transition]


def count_transition_errors(trace_summary: dict) -> None:
    """Count how many model/log moves exist with a particular transition.

    Args:
        trace_summary (dict): shortend summary list
    """
    for trace_id in trace_summary:
        transition_errors = trace_summary[trace_id]['cost']
        alignment = trace_summary[trace_id]['alignment']
        trace_count = trace_summary[trace_id]['count']

        if alignment:
            for match in alignment:
                activity_skip = contains_skip(match)
                if activity_skip:
                    transition_errors[activity_skip] += trace_count
                    trace_summary[trace_id]['fit'] = False
        else:
            trace_summary[trace_id]['fit'] = False


def get_alignment(sublog: List[Trace],
                  petri: Tuple[PetriNet, Marking, Marking]):
    """Get the alignment for every trace in the sublog on the net fragment.

    Returns:
        List[List[Tuple[str, str]]]: List of alignments from all traces.
    """
    net, im, fm = petri
    for i, trace_id in enumerate(sublog):
        trace = sublog[trace_id]['trace']
        if trace:
            trace_align = apply_trace(trace, net, im, fm,
                                      variant=VERSION_DIJKSTRA_NO_HEURISTICS)
            sublog[trace_id]['alignment'] = trace_align['alignment']
        else:
            sublog[trace_id]['alignment'] = None


def get_global_fitness(local_align: dict,
                       log: EventLog,
                       whole_model: Tuple[PetriNet, Marking, Marking]) -> dict:
    """Calculates the global alignment fitness value using all of the costs
    from the adapted local alignments. In addition, return the percentage of
    fitting traces.

    Args:
        local_align (dict): local alignment dictionary
        log (EventLog): Whole event log used to calculate denominator
        whole_model (Tuple[PetriNet, Marking, Marking]): whole model used to
        get the best worst case alignment

    Returns:
        dict: dictionary containing the fitness and percentage of perfectly
            fitting traces.
    """
    trace_number = len(log)
    event_number = get_event_count(log)
    empty_trace_number = entire_trace_gone_number(local_align)
    best_worst_cost = get_minimum_distance(whole_model)
    passage_costs = sum_costs(local_align) + \
        account_missing_labels(local_align, event_number) + \
        (best_worst_cost * empty_trace_number)

    # print(passage_costs, alignments_denominator(trace_number,
    #                                             sum(event_number.values()),
    #                                             best_worst_cost))

    fitness = 1 - (passage_costs /
                   alignments_denominator(trace_number,
                                          sum(event_number.values()),
                                          best_worst_cost))

    fitting_traces_percentage = get_fitting_trace_percentage(local_align)

    return {'fitness': fitness, 'percFitTraces': fitting_traces_percentage}


def account_missing_labels(local_align: dict, event_count: dict) -> int:
    """Accounts for move on log moves of labels that do not exist in the petri
    net. As each alignment check only runs on transitions that exist on the
    model, we can sum all the non-existant transitions and count them as log
    moves by using the event count dictionary to get the number of events
    that happened with these missing transitions.

    Args:
        local_align (dict): local alignment dictionary.
        event_count (dict): dictionary of log transition counts.

    Returns:
        int: number of log moves due to model missing transition.
    """
    model_t = set()
    additional_cost = 0
    for f in local_align:
        model_t |= {t.label for t in local_align[f]['petri'][0].transitions
                    if t}

    for k, v in event_count.items():
        if k not in model_t:
            additional_cost += v

    return additional_cost


def alignments_denominator(trace_number: int,
                           event_number: int,
                           best_worst_distance: int) -> float:
    """Calculates the denominator of the alignment calculation. This is done by
    the following equation:
    num_events_in_log + (num_trace_in_log * best_worst_alignment).

    Returns:
        float: fitness value
    """
    return event_number + (trace_number * best_worst_distance)


def get_minimum_distance(petri: Tuple[PetriNet, Marking, Marking]) -> int:
    """Get the minimum number of model moves in order to go through
    the entire petri net (from initial marking to final marking).

    Args:
        petri (Tuple[PetriNet, Marking, Marking]): Petri net to traverse.

    Returns:
        int: Minimum number of model moves to get to the final marking.
    """
    return get_best_worst_cost(petri[0], petri[1], petri[2])


def get_event_count(log: EventLog) -> int:
    """Calculates the number of events in an event log.

    Args:
        log (EventLog): Event log to analyse

    Returns:
        int: Number of events in event log
    """
    event_count = dict()
    for trace in log:
        for event in trace:
            event_name = event['concept:name']
            if event_name not in event_count:
                event_count[event_name] = 1
            else:
                event_count[event_name] += 1

    return event_count


def sum_costs(local_align: dict) -> float:
    """Sum the costs of all adapted local alignments from each net fragment.

    Args:
        local_align (dict): local alignment dictionary

    Returns:
        float: total global cost from all input net fragment alignments
    """
    total_cost = 0.0
    for f in local_align:
        total_cost += sum(local_align[f]['costs'].values())

    return total_cost


def entire_trace_gone_number(local_align: dict) -> int:
    """Get the count of traces that are entirely non-fitting to the event log.
    This consists of traces where none of the transitions are in the model.

    Args:
        local_align (dict): Local alignment object

    Returns:
        int: Number of empty traces
    """
    empty_traces = set()
    for f in local_align:
        if not local_align[f]['unfit_traces']:
            return 0
        elif empty_traces:
            empty_traces &= local_align[f]['unfit_traces']
        else:
            empty_traces = local_align[f]['unfit_traces']

    return len(empty_traces)


def get_fitting_trace_percentage(local_align: dict) -> float:
    """Calculates the percentage of fitting traces globally.

    Args:
        local_align (dict): local alignment dictionary

    Returns:
        float: Percentage of global perfectly fitting traces.
    """
    trace_number = len(local_align[0]['sublog'])
    unfit_traces = set()
    for f in local_align:
        unfit_traces |= local_align[f]['unfit_traces']

    return 1 - (len(unfit_traces) / trace_number)


def contains_skip(activity: Tuple[str, str]) -> str:
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
            if activity[0] is not None:
                return activity[0]
        elif activity[1] is not None:
            return activity[1]

    return None


def remove_empty_traces(log: EventLog) -> None:
    """Remove all empty traces in event log (in place).

    Args:
        log (EventLog): target event log to filter
    """
    log._list = [trace for i, trace in enumerate(log) if trace]
