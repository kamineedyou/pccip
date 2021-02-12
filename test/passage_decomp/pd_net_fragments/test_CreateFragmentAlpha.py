import pytest
import os
import re
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.petri.importer import importer as pnml_importer
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.log.log import Trace
from passage_decomp.pd.logToFragments import create_fragment


class Test_CreateFragmentAlpha:
    @pytest.fixture
    def loopStartThenParallel(self):
        file_list = ['abcdf.xes']
        sublog_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'logs/' + f)
            sublog_list.append(xes_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'models/abcdf.pnml')
        expected = pnml_importer.apply(pathToFile)
        return sublog_list, expected

    @pytest.fixture
    def loopEndWithOrSplit(self):
        file_list = ['efgh.xes']
        sublog_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'logs/' + f)
            sublog_list.append(xes_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'models/efgh.pnml')
        expected = pnml_importer.apply(pathToFile)

        return sublog_list, expected

    @pytest.fixture
    def startOfLog(self):
        file_list = ['TOPa.xes']
        sublog_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'logs/' + f)
            sublog_list.append(xes_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'models/TOPa.pnml')
        expected = pnml_importer.apply(pathToFile)

        return sublog_list, expected

    @pytest.fixture
    def endOfLog(self):
        file_list = ['ghBOT.xes']
        sublog_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'logs/' + f)
            sublog_list.append(xes_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'models/ghBOT.pnml')
        expected = pnml_importer.apply(pathToFile)

        return sublog_list, expected

    def test_FragLoopParallel(self, loopStartThenParallel):
        sublog = loopStartThenParallel[0][0]
        exp_net, exp_im, exp_fm = loopStartThenParallel[1]
        exp_places = [sorted([x for x in re.split("[^a-zA-Z]*", p.name) if x])
                      for p in exp_net.places]
        exp_transitions = {str(x) for x in exp_net.transitions}
        exp_arcs = [sorted([x for x in re.split("[^a-zA-Z]*", str(a)) if x])
                    for a in exp_net.arcs]

        new_frag, new_im, new_fm = create_fragment(sublog,
                                                   variant='ALPHA')

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

    def test_FragLoopWithOrSplit(self, loopEndWithOrSplit):
        sublog = loopEndWithOrSplit[0][0]
        exp_net, exp_im, exp_fm = loopEndWithOrSplit[1]
        exp_places = [sorted([x for x in re.split("[^a-zA-Z]*", p.name) if x])
                      for p in exp_net.places]
        exp_transitions = {str(x) for x in exp_net.transitions}
        exp_arcs = [sorted([x for x in re.split("[^a-zA-Z]*", str(a)) if x])
                    for a in exp_net.arcs]

        new_frag, new_im, new_fm = create_fragment(sublog,
                                                   variant='ALPHA')

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

    def test_FragStart(self, startOfLog):
        sublog = startOfLog[0][0]
        exp_net, exp_im, exp_fm = startOfLog[1]
        exp_places = [sorted([x for x in re.split("[^a-zA-Z]*", p.name) if x])
                      for p in exp_net.places]
        exp_transitions = {str(x) for x in exp_net.transitions}
        exp_arcs = [sorted([x for x in re.split("[^a-zA-Z]*", str(a)) if x])
                    for a in exp_net.arcs]

        new_frag, new_im, new_fm = create_fragment(sublog,
                                                   variant='ALPHA')

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

    def test_FragEnd(self, endOfLog):
        sublog = endOfLog[0][0]
        exp_net, exp_im, exp_fm = endOfLog[1]
        exp_places = [sorted([x for x in re.split("[^a-zA-Z]*", p.name) if x])
                      for p in exp_net.places]
        exp_transitions = {str(x) for x in exp_net.transitions}
        exp_arcs = [sorted([x for x in re.split("[^a-zA-Z]*", str(a)) if x])
                    for a in exp_net.arcs]

        new_frag, new_im, new_fm = create_fragment(sublog,
                                                   variant='ALPHA')

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
