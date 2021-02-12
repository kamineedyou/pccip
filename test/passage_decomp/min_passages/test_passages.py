import pytest
import os
from networkx import DiGraph
from passage_decomp.passages.passage import Passage
from pm4py.objects.petri.petrinet import PetriNet
from pm4py.objects.petri.importer import importer as pn_importer


class Test_Passages:
    @pytest.fixture
    def validPassage(self):
        # from figure 2 in paper
        causal_example = {('d', 'd'), ('d', 'e'), ('b', 'e'),
                          ('b', 'd'), ('b', 'f'), ('c', 'f')}

        return Passage(causal_example)

    @pytest.fixture
    def validPassages(self):
        # from figure 2 in paper
        passage_list = [Passage({('b', 'f'), ('d', 'e'), ('c', 'f'),
                                 ('b', 'e'), ('d', 'd'), ('b', 'd')}),
                        Passage({('e', 'g')}),
                        Passage({('a', 'c'), ('a', 'b')}),
                        Passage({('h', 'i'), ('g', 'i')}),
                        Passage({('f', 'h')})]

        return passage_list

    @pytest.fixture
    def validDiGraph(self):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'figure1.pnml')
        net, *_ = pn_importer.apply(pathToFile)
        skeleton = DiGraph()
        for place in net.places:
            for arcIn in place.in_arcs:
                for arcOut in place.out_arcs:
                    skeleton.add_edge(arcIn.source, arcOut.target)
        return skeleton, net

    def test_ValidPassageInit(self, validPassage):

        assert isinstance(validPassage, Passage)
        assert ('d', 'e') in validPassage.edges
        assert len(validPassage.edges) == 6

        passage_2 = Passage()
        assert isinstance(passage_2, Passage)
        assert validPassage != passage_2

    def test_InvalidPassageInit(self):
        with pytest.raises(TypeError):
            Passage(('a', 'b'))

    def test_ValidPassageGetX(self, validPassage):
        test_object = validPassage.getX()
        assert isinstance(test_object, set)
        assert len(test_object) == 3
        assert 'd' in test_object and 'b' in test_object and 'c' in test_object

    def test_ValidPassageGetY(self, validPassage):
        test_object = validPassage.getY()
        assert isinstance(test_object, set)
        assert len(test_object) == 3
        assert 'd' in test_object and 'e' in test_object and 'f' in test_object

    def test_ValidPassageGetXY(self, validPassage):
        test_X, test_Y = validPassage.getXY()
        assert isinstance(test_X, set)
        assert isinstance(test_Y, set)
        assert len(test_X) == 3
        assert len(test_Y) == 3
        assert 'd' in test_X and 'b' in test_X and 'c' in test_X
        assert 'd' in test_Y and 'e' in test_Y and 'f' in test_Y

    def test_ValidPassageAddEdge(self, validPassage):
        test_add = ('a', 'b')
        test_add_set = {('a', 'b')}
        test_add_wrong_edge0 = (2, 'b')

        assert len(validPassage.edges) == 6
        validPassage.addEdge(test_add)
        assert len(validPassage.edges) == 7
        assert test_add in validPassage.edges
        validPassage.addEdge(test_add)
        assert len(validPassage.edges) == 7

        with pytest.raises(TypeError):
            validPassage.addEdge(test_add_set)
            validPassage.addEdge(test_add_wrong_edge0)

    def test_ValidPassageMagicAddSub(self, validPassage):
        test_pass = Passage({('x', 'y')})
        test_invalid = {('x', 'y')}
        new_passage = validPassage + test_pass
        assert new_passage != validPassage
        new_passage = new_passage - test_pass
        assert new_passage == validPassage
        # test if it stays the same if removed again
        new_passage = new_passage - test_pass
        assert new_passage == validPassage

        # add required both to be Passages
        with pytest.raises(TypeError):
            test_pass + test_invalid
            test_pass - test_invalid

    def test_ValidPassageBorderCheck(self, validPassages):
        big_passage = validPassages[0]
        start_passage = validPassages[2]
        combined_passage = big_passage + start_passage
        assert big_passage.getBorderX() == {'c', 'b'}
        assert big_passage.getBorderY() == {'e', 'f'}
        assert start_passage.getBorderX() == {'a'}
        assert start_passage.getBorderY() == {'b', 'c'}
        assert combined_passage.getBorderX() == {'a'}
        assert combined_passage.getBorderY() == {'e', 'f'}

        # making sure loops at border dont interfere with border check
        # Before: X={'a'}, Y={'b', 'c'}
        # After: X={'a', 'c'}, Y={'a', 'b', 'c'}
        loop_passage = start_passage + Passage({('a', 'a'), ('c', 'c')})
        assert loop_passage.getBorderX() == {'a'}
        assert loop_passage.getBorderY() == {'b', 'c'}

    def test_GetVisibleTransitions(self, validPassages):
        passage_list = validPassages
        expected_t_vis = [['b', 'c', 'd', 'e', 'f'],
                          ['e', 'g'],
                          ['a', 'b', 'c'],
                          ['g', 'h', 'i'],
                          ['f', 'h']]

        for index, passage in enumerate(passage_list):
            assert sorted(passage.getTVis()) == sorted(expected_t_vis[index])

    def test_DiGraphImport(self, validDiGraph):
        passage = Passage(validDiGraph[0])
        exp_net = validDiGraph[1]

        for edge in passage.edges:
            assert edge in set(passage.digraph_link.keys())
            assert isinstance(edge, tuple)
            assert isinstance(edge[0], str)
            assert isinstance(edge[1], str)

        assert passage.getBorderX() == {'a'}
        assert passage.getBorderY() == {'g', 'h'}

        for transition in exp_net.transitions:
            tran = passage.get_digraph_transition(transition.name)
            assert tran is not None
            assert isinstance(tran, PetriNet.Transition)

        for edge in passage.edges:
            di_edge = passage.get_digraph_edge(edge)
            assert di_edge is not None
            assert isinstance(di_edge, tuple)
            assert isinstance(di_edge[0], PetriNet.Transition)
            assert isinstance(di_edge[1], PetriNet.Transition)
            assert di_edge in validDiGraph[0].edges
