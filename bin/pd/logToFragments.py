
from enum import Enum
from pm4py.objects.log.log import EventLog, Trace
from pm4py.objects.petri.petrinet import PetriNet
from pm4py.algo.discovery.alpha.algorithm import apply as alpha_algo
from pm4py.statistics.start_activities.log.get import get_start_activities
from pm4py.statistics.end_activities.log.get import get_end_activities
from pm4py.objects.petri.utils import remove_place


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
            if event['concept:name'] in start_activities \
                and index > last_loop \
                    and prev_event not in start_activities:
                split_log.append(Trace(trace[last_loop:index]))
                last_loop = index
            elif event['concept:name'] in end_activities \
                and index < len(trace) - 1 \
                    and prev_event not in end_activities:
                split_log.append(Trace(trace[last_loop:index+1]))
                last_loop = index + 1
            prev_event = event['concept:name']
        split_log.append(trace[last_loop:])

    return split_log


class Variants(Enum):
    DEFAULT_VARIANT = alpha_fragments
    ALPHA = alpha_fragments


def create_fragments(sublog: EventLog,
                     parameters: dict = None,
                     variant: Variants = Variants.DEFAULT_VARIANT) -> PetriNet:
    if parameters is None:
        parameters = {}

    new_log = split_log(sublog)
    net, im, fm = variant(sublog=new_log, parameters=parameters)
    remove_place(net, next(iter(im.keys())))
    remove_place(net, next(iter(fm.keys())))
    return net
