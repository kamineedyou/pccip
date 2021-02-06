import pytest
import os
import re
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.petri.importer import importer as pnml_importer
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.log.log import Trace
from pccip.bin.pd.logToFragments import create_fragment


class Test_CreateFragmentInductive:
    @pytest.fixture
    def inductive_start(self):
        file_list = ['TOPa.xes']
        sublog_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'logs/' + f)
            sublog_list.append(xes_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'models/inductive_start.pnml')
        expected = pnml_importer.apply(pathToFile)

        return sublog_list, expected

    @pytest.fixture
    def inductive_silent_start(self):
        file_list = ['bcde.xes']
        sublog_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'logs/' + f)
            sublog_list.append(xes_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir,
                                  'models/inductive_silent_start.pnml')
        expected = pnml_importer.apply(pathToFile)

        return sublog_list, expected

    @pytest.fixture
    def inductive_silent_end(self):
        file_list = ['abcdf.xes']
        sublog_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'logs/' + f)
            sublog_list.append(xes_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir,
                                  'models/inductive_silent_end.pnml')
        expected = pnml_importer.apply(pathToFile)

        return sublog_list, expected

    @pytest.fixture
    def inductive_end(self):
        file_list = ['ghBOT.xes']
        sublog_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'logs/' + f)
            sublog_list.append(xes_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'models/inductive_end.pnml')
        expected = pnml_importer.apply(pathToFile)

        return sublog_list, expected

    def test_inductive_start(self, inductive_start):
        sublog = inductive_start[0][0]
        exp_net, exp_im, exp_fm = inductive_start[1]
        exp_places = [sorted(
            [x for x in re.split("[^a-zA-Z]*", p.name[:-5])
             if x]) for p in exp_net.places]
        exp_transitions = {str(x) for x in exp_net.transitions}
        exp_arcs = [sorted([x for x in re.split("[^a-zA-Z]*", str(a)) if x])
                    for a in exp_net.arcs]

        new_frag, new_im, new_fm = create_fragment(sublog,
                                                   variant='INDUCTIVE')

        for place in new_frag.places:
            place.name = place.name[:-5]

        assert isinstance(new_frag, PetriNet)
        assert isinstance(new_im, Marking)
        assert isinstance(new_fm, Marking)

        # check all transitions
        assert len(exp_net.transitions) == len(new_frag.transitions)
        for transition in new_frag.transitions:
            assert isinstance(transition, PetriNet.Transition)
            assert str(transition) in exp_transitions

        # check all places
        assert len(exp_net.places) == len(new_frag.places)
        for place in new_frag.places:
            assert isinstance(place, PetriNet.Place)
            assert sorted([x for x in re.split("[^a-zA-Z]*",
                                               place.name) if x]) in exp_places

        # check all arcs
        assert len(exp_net.arcs) == len(new_frag.arcs)
        for arc in new_frag.arcs:
            assert isinstance(arc, PetriNet.Arc)
            assert sorted([x for x in re.split("[^a-zA-Z]*",
                                               str(arc)) if x]) in exp_arcs

        assert len(new_im.keys()) == len(exp_im.keys())
        assert len(new_fm.keys()) == len(exp_fm.keys())

    def test_inductive_silent_start(self, inductive_silent_start):
        sublog = inductive_silent_start[0][0]
        exp_net, exp_im, exp_fm = inductive_silent_start[1]
        exp_places = [sorted(
            [x for x in re.split("[^a-zA-Z]*", p.name[:-5])
             if x]) for p in exp_net.places]
        exp_transitions = {str(x) for x in exp_net.transitions}
        exp_arcs = [sorted([x for x in re.split("[^a-zA-Z]*", str(a)) if x])
                    for a in exp_net.arcs]

        new_frag, new_im, new_fm = create_fragment(sublog,
                                                   variant='INDUCTIVE')

        for place in new_frag.places:
            place.name = place.name[:-5]

        assert isinstance(new_frag, PetriNet)
        assert isinstance(new_im, Marking)
        assert isinstance(new_fm, Marking)

        # check all transitions
        assert len(exp_net.transitions) == len(new_frag.transitions)
        for transition in new_frag.transitions:
            assert isinstance(transition, PetriNet.Transition)
            assert str(transition) in exp_transitions

        # check all places
        assert len(exp_net.places) == len(new_frag.places)
        for place in new_frag.places:
            assert isinstance(place, PetriNet.Place)
            assert sorted([x for x in re.split("[^a-zA-Z]*",
                                               place.name) if x]) in exp_places

        # check all arcs
        assert len(exp_net.arcs) == len(new_frag.arcs)
        for arc in new_frag.arcs:
            assert isinstance(arc, PetriNet.Arc)
            assert sorted([x for x in re.split("[^a-zA-Z]*",
                                               str(arc)) if x]) in exp_arcs

        assert len(new_im.keys()) == len(exp_im.keys())
        assert len(new_fm.keys()) == len(exp_fm.keys())

    def test_inductive_silent_end(self, inductive_silent_end):
        sublog = inductive_silent_end[0][0]
        exp_net, exp_im, exp_fm = inductive_silent_end[1]
        exp_places = [sorted(
            [x for x in re.split("[^a-zA-Z]*", p.name[:-5])
             if x]) for p in exp_net.places]
        exp_transitions = {str(x) for x in exp_net.transitions}
        exp_arcs = [sorted([x for x in re.split("[^a-zA-Z]*", str(a)) if x])
                    for a in exp_net.arcs]

        new_frag, new_im, new_fm = create_fragment(sublog,
                                                   variant='INDUCTIVE')

        for place in new_frag.places:
            place.name = place.name[:-5]

        assert isinstance(new_frag, PetriNet)
        assert isinstance(new_im, Marking)
        assert isinstance(new_fm, Marking)

        # check all transitions
        assert len(exp_net.transitions) == len(new_frag.transitions)
        for transition in new_frag.transitions:
            assert isinstance(transition, PetriNet.Transition)
            assert str(transition) in exp_transitions

        # check all places
        assert len(exp_net.places) == len(new_frag.places)
        for place in new_frag.places:
            assert isinstance(place, PetriNet.Place)
            assert sorted([x for x in re.split("[^a-zA-Z]*",
                                               place.name) if x]) in exp_places

        # check all arcs
        assert len(exp_net.arcs) == len(new_frag.arcs)
        for arc in new_frag.arcs:
            assert isinstance(arc, PetriNet.Arc)
            assert sorted([x for x in re.split("[^a-zA-Z]*",
                                               str(arc)) if x]) in exp_arcs

        assert len(new_im.keys()) == len(exp_im.keys())
        assert len(new_fm.keys()) == len(exp_fm.keys())

    def test_inductive_end(self, inductive_end):
        sublog = inductive_end[0][0]
        exp_net, exp_im, exp_fm = inductive_end[1]
        exp_places = [sorted(
            [x for x in re.split("[^a-zA-Z]*", p.name[:-5])
             if x]) for p in exp_net.places]
        exp_transitions = {str(x) for x in exp_net.transitions}
        exp_arcs = [sorted([x for x in re.split("[^a-zA-Z]*", str(a)) if x])
                    for a in exp_net.arcs]

        new_frag, new_im, new_fm = create_fragment(sublog,
                                                   variant='INDUCTIVE')

        for place in new_frag.places:
            place.name = place.name[:-5]

        assert isinstance(new_frag, PetriNet)
        assert isinstance(new_im, Marking)
        assert isinstance(new_fm, Marking)

        # check all transitions
        assert len(exp_net.transitions) == len(new_frag.transitions)
        for transition in new_frag.transitions:
            assert isinstance(transition, PetriNet.Transition)
            assert str(transition) in exp_transitions

        # check all places
        assert len(exp_net.places) == len(new_frag.places)
        for place in new_frag.places:
            assert isinstance(place, PetriNet.Place)
            assert sorted([x for x in re.split("[^a-zA-Z]*",
                                               place.name) if x]) in exp_places

        # check all arcs
        assert len(exp_net.arcs) == len(new_frag.arcs)
        for arc in new_frag.arcs:
            assert isinstance(arc, PetriNet.Arc)
            assert sorted([x for x in re.split("[^a-zA-Z]*",
                                               str(arc)) if x]) in exp_arcs

        assert len(new_im.keys()) == len(exp_im.keys())
        assert len(new_fm.keys()) == len(exp_fm.keys())

    def test_InvalidInput(self):
        with pytest.raises(TypeError):
            create_fragment('<xml>event log</xml>')
            create_fragment(Trace())
