import os
import pytest
from pm4py.objects.petri.petrinet import PetriNet
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.conformance.alignments import algorithm as alignments
from pccip.bin.cc.EventLogDecomp import decompose_event_log
from pccip.bin.cc import Adapted_Cost


@pytest.mark.parametrize(('tupl, result'),
                         [(('a', 'b'), None),
                         (('a', '>>'), 'a'),
                         (('a', None), None)
                         ])

def test_Get_Acti(tupl, result):
    assert Adapted_Cost.Get_Acti(tupl) == result


@pytest.fixture
def net_frag():
    currentDir = os.path.dirname(os.path.realpath(__file__))
    pathToFile_1 = os.path.join(currentDir, 'figure8_mod_orig.xes')
    pathToFile_2 = os.path.join(currentDir, 'figure8_mod.xes')
    log_1 = xes_importer.apply(pathToFile_1)
    log_2 = xes_importer.apply(pathToFile_2)
    net, initial_marking, final_marking = inductive_miner.apply(log_1)
    aligned_transition = alignments.apply_log(log_2, net, initial_marking, final_marking)
    return aligned_transition

def test_Get_Misaligned(net_frag):
    result = Adapted_Cost.Get_Misaligned_Trans(net_frag)
    assert result == [{'a', 'b'}]

@pytest.fixture
def nnet_fragments():
    currentDir = os.path.dirname(os.path.realpath(__file__))
    pathToFile = os.path.join(currentDir, 'figure8_mod.xes')
    log = xes_importer.apply(pathToFile)
    sub_log_1 = decompose_event_log(log, ['a', 'b', 'c'])
    sub_log_2 = decompose_event_log(log, ['b', 'c', 'd'])

    net_1 = PetriNet("petri_net_1")
    source_1 = PetriNet.Place("source")
    sink_1 = PetriNet.Place("sink")
    c_1 = PetriNet.Place("c_1")
    net_1.places.add(source_1)
    net_1.places.add(sink_1)
    net_1.places.add(c_1)
    t_11 = PetriNet.Transition("name_1", "a")
    t_12 = PetriNet.Transition("name_2", "b")
    t_13 = PetriNet.Transition("name_3", "c")
    net_1.transitions.add(t_11)
    net_1.transitions.add(t_12)
    net_1.transitions.add(t_13)
    from pm4py.objects.petri import utils
    utils.add_arc_from_to(source_1, t_11, net_1)
    utils.add_arc_from_to(source_1, t_13, net_1)
    utils.add_arc_from_to(t_11, c_1, net_1)
    utils.add_arc_from_to(c_1, t_12, net_1)
    utils.add_arc_from_to(t_12, sink_1, net_1)
    utils.add_arc_from_to(t_13, sink_1, net_1)
#second fragment
    net_2 = PetriNet("petri_net_2")
    source_2 = PetriNet.Place("source")
    sink_2 = PetriNet.Place("sink")
    c_2 = PetriNet.Place("c_2")
    net_2.places.add(sink_2)
    net_2.places.add(source_2)
    net_2.places.add(c_2)
    t_21 = PetriNet.Transition("n_1", "d")
    t_22 = PetriNet.Transition("n_2", "b")
    t_23 = PetriNet.Transition("n_3", "c")
    net_2.transitions.add(t_21)
    net_2.transitions.add(t_22)
    net_2.transitions.add(t_23)
    from pm4py.objects.petri import utils
    utils.add_arc_from_to(source_2, t_22, net_2)
    utils.add_arc_from_to(source_2, t_23, net_2)
    utils.add_arc_from_to(t_23, c_2, net_2)
    utils.add_arc_from_to(c_2, t_21, net_2)
    utils.add_arc_from_to(t_21, sink_2, net_2)
    utils.add_arc_from_to(t_22, sink_2, net_2)
    net_log = [sub_log_1, sub_log_2]
    net_frag = [net_1, net_2]
    return net_log, net_frag

def test_adapted_cost_fun(nnet_fragments):
    align_trace, average_fitness = Adapted_Cost.Adapted_Cost_func(nnet_fragments[0], nnet_fragments[1])
    assert align_trace[1][0]['cost'] == 0.5
