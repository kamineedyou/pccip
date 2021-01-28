from enum import Enum
from pm4py.objects.log.log import EventLog, Trace
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.algo.discovery.alpha.algorithm import apply as alpha_algo
from pm4py.statistics.start_activities.log.get import get_start_activities
from pm4py.statistics.end_activities.log.get import get_end_activities
from pm4py.objects.petri.utils import remove_place, merge, remove_transition


def alpha_fragments(sublog: EventLog, parameters: dict = None) -> PetriNet:
    return alpha_algo(sublog, parameters=parameters)


def split_log(sublog: EventLog):
    start_activities = set(get_start_activities(sublog).keys())
    end_activities = set(get_end_activities(sublog).keys())
    split_log = EventLog()

    for trace in sublog:
        last_loop = 0
        prev_event = None
        for index, event in enumerate(trace):
            curr_event = event['concept:name']
            if index < len(trace) - 1:
                next_event = trace[index+1]['concept:name']
            else:
                next_event = None

            if curr_event in start_activities \
                and index > last_loop \
                    and prev_event not in start_activities:
                split_log.append(Trace(trace[last_loop:index]))
                last_loop = index
            elif curr_event in end_activities \
                and index < len(trace) - 1 \
                    and next_event not in end_activities:
                split_log.append(Trace(trace[last_loop:index+1]))
                last_loop = index + 1
            prev_event = curr_event
        split_log.append(trace[last_loop:])

    return split_log


class Variants(Enum):
    DEFAULT_VARIANT = alpha_fragments
    ALPHA = alpha_fragments


def create_fragment(sublog: EventLog,
                    parameters: dict = None,
                    variant: Variants = Variants.DEFAULT_VARIANT) -> PetriNet:
    if parameters is None:
        parameters = {}

    new_log = split_log(sublog)
    net, im, fm = variant(sublog=new_log, parameters=parameters)

    initial_marking = Marking()
    final_marking = Marking()
    im_place = next(iter(im.keys()))
    fm_place = next(iter(fm.keys()))

    # Create new Marking if fragment is the start fragment
    if len(im_place.out_arcs) == 1:
        im_transition = next(iter(im_place.out_arcs)).target
        if im_transition.label == 'Artificial:Start':
            new_im_place = next(iter(im_transition.out_arcs)).target
            remove_place(net, im_place)
            remove_transition(net, im_transition)
            initial_marking = Marking({new_im_place: 1})

    # Create new Marking if fragment is the end fragment
    if len(fm_place.in_arcs) == 1:
        fm_transition = next(iter(fm_place.in_arcs)).source
        if fm_transition.label == 'Artificial:End':
            new_fm_place = next(iter(fm_transition.in_arcs)).source
            remove_place(net, fm_place)
            remove_transition(net, fm_transition)
            final_marking = Marking({new_fm_place: 1})

    if not len(initial_marking):
        remove_place(net, im_place)
    if not len(final_marking):
        remove_place(net, fm_place)

    return net, initial_marking, final_marking


def merge_fragments(fragments: list) -> PetriNet:
    final_net = merge(nets=fragments)
    for net, im, fm in fragments:
        if len(im):
            initial_marking = im
        if len(fm):
            final_marking = fm

    return final_net, initial_marking, final_marking
