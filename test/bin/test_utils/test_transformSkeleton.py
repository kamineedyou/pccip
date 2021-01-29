from pccip.bin.utils.transformSkeleton import petriNetIntoSkeleton
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.petri import utils


class TestSkeleton:

    def test_PetriNetIntoSkeleton(self):
        net = PetriNet("NotWorkflowNet")
        source = PetriNet.Place("source")
        source2 = PetriNet.Place("source2")
        sink = PetriNet.Place("sink")
        p_1 = PetriNet.Place("p_1")
        # add them to the net
        net.places.add(source)
        net.places.add(sink)
        net.places.add(p_1)
        net.places.add(source2)
        # create transitions
        t_1 = PetriNet.Transition("name_1", "label_1")
        t_2 = PetriNet.Transition("name_2", "label_2")
        # Add the transitions to the Petri Net
        net.transitions.add(t_1)
        net.transitions.add(t_2)
        # Add arcs
        utils.add_arc_from_to(source, t_1, net)
        utils.add_arc_from_to(t_1, p_1, net)
        utils.add_arc_from_to(p_1, t_2, net)
        utils.add_arc_from_to(t_2, sink, net)
        utils.add_arc_from_to(source2, t_1, net)

        # Adding tokens
        initial_marking = Marking()
        initial_marking[source] = 1
        initial_marking[source2] = 1
        final_marking = Marking()
        final_marking[sink] = 1
        skeleton = petriNetIntoSkeleton(net)
        assert set(skeleton.edges) == set([(t_1, t_2)])
