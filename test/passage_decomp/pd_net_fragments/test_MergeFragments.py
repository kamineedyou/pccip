import pytest
import os
import re
from pm4py.objects.petri.importer import importer as pnml_importer
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pccip.passage_decomp.pd.logToFragments import merge_fragments


class Test_MergeFragments:
    @pytest.fixture
    def startMiddle(self):
        file_list = ['TOPa.pnml', 'abcdf.pnml']
        fragment_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'models/' + f)
            fragment_list.append(pnml_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'models/TOPabcdf.pnml')
        expected = pnml_importer.apply(pathToFile)
        return fragment_list, expected

    @pytest.fixture
    def middleEnd(self):
        file_list = ['efgh.pnml', 'ghBOT.pnml']
        fragment_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'models/' + f)
            fragment_list.append(pnml_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'models/efghBOT.pnml')
        expected = pnml_importer.apply(pathToFile)

        return fragment_list, expected

    @pytest.fixture
    def middleOnly(self):
        file_list = ['abcdf.pnml', 'bcde.pnml']
        fragment_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'models/' + f)
            fragment_list.append(pnml_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'models/abcdef.pnml')
        expected = pnml_importer.apply(pathToFile)

        return fragment_list, expected

    @pytest.fixture
    def whole(self):
        file_list = ['TOPa.pnml', 'abcdf.pnml',
                     'bcde.pnml', 'efgh.pnml', 'ghBOT.pnml']
        fragment_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'models/' + f)
            fragment_list.append(pnml_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'models/figure1.pnml')
        expected = pnml_importer.apply(pathToFile)

        return fragment_list, expected

    def test_MergeStartMiddle(self, startMiddle):
        fragment_list = startMiddle[0]
        exp_net, exp_im, exp_fm = startMiddle[1]
        exp_places = [sorted(
            [x for x in re.split("[^a-zA-Z]*", p.name[:-5])
             if x]) for p in exp_net.places]
        exp_transitions = {str(x) for x in exp_net.transitions}
        exp_arcs = [sorted([x for x in re.split("[^a-zA-Z]*", str(a)) if x])
                    for a in exp_net.arcs]

        new_frag, new_im, new_fm = merge_fragments(fragment_list)

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

    def test_MergeMiddleEnd(self, middleEnd):
        fragment_list = middleEnd[0]
        exp_net, exp_im, exp_fm = middleEnd[1]
        exp_places = [sorted(
            [x for x in re.split("[^a-zA-Z]*", p.name[:-5])
             if x]) for p in exp_net.places]
        exp_transitions = {str(x) for x in exp_net.transitions}
        exp_arcs = [sorted([x for x in re.split("[^a-zA-Z]*", str(a)) if x])
                    for a in exp_net.arcs]

        new_frag, new_im, new_fm = merge_fragments(fragment_list)

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

    def test_MergeMiddleOnly(self, middleOnly):
        fragment_list = middleOnly[0]
        exp_net, exp_im, exp_fm = middleOnly[1]
        exp_places = [sorted(
            [x for x in re.split("[^a-zA-Z]*", p.name[:-5])
             if x]) for p in exp_net.places]
        exp_transitions = {str(x) for x in exp_net.transitions}
        exp_arcs = [sorted([x for x in re.split("[^a-zA-Z]*", str(a)) if x])
                    for a in exp_net.arcs]

        new_frag, new_im, new_fm = merge_fragments(fragment_list)

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

    def test_MergeWhole(self, whole):
        fragment_list = whole[0]
        exp_net, exp_im, exp_fm = whole[1]
        exp_places = [sorted(
            [x for x in re.split("[^a-zA-Z]*", p.name[:-5])
             if x]) for p in exp_net.places]
        exp_transitions = {str(x) for x in exp_net.transitions}
        exp_arcs = [sorted([x for x in re.split("[^a-zA-Z]*", str(a)) if x])
                    for a in exp_net.arcs]

        new_frag, new_im, new_fm = merge_fragments(fragment_list)

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
            merge_fragments([PetriNet(), PetriNet()])
            merge_fragments([('PetriNet', 'im', 'fm')])
