import pytest
import os
from networkx import DiGraph
from pccip.bin.passages.passage import Passage
from pccip.bin.passages.min_passages import algorithm, pi_1, pi_2, pi_both
from pm4py.objects.petri.importer import importer as pn_importer


class Test_Min_Passages:
    @pytest.fixture
    def validCausal(self):
        # from figure 2 in paper
        causal_example = {('d', 'd'), ('d', 'e'), ('b', 'e'),
                          ('b', 'd'), ('b', 'f'), ('c', 'f'),
                          ('a', 'b'), ('a', 'c'), ('e', 'g'),
                          ('f', 'h'), ('g', 'i'), ('h', 'i')}

        causal_expected = {Passage({('b', 'f'), ('d', 'e'), ('c', 'f'),
                                    ('b', 'e'), ('d', 'd'), ('b', 'd')}),
                           Passage({('e', 'g')}),
                           Passage({('a', 'c'), ('a', 'b')}),
                           Passage({('h', 'i'), ('g', 'i')}),
                           Passage({('f', 'h')})}

        return causal_example, causal_expected

    @pytest.fixture
    def validCausal2(self):
        # from figure 8 in paper
        causal_example = {('Artificial:Start', 'a'), ('Artificial:Start', 'c'),
                          ('a', 'b'), ('c', 'd'), ('b', 'Artificial:End'),
                          ('d', 'Artificial:End')}

        causal_expected = {Passage({('Artificial:Start', 'a'),
                                    ('Artificial:Start', 'c')}),
                           Passage({('a', 'b')}),
                           Passage({('c', 'd')}),
                           Passage({('b', 'Artificial:End'),
                                    ('d', 'Artificial:End')})}

        return causal_example, causal_expected

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

        expected = {'getX': [{'e'}, {'a', 'f'}, {'b', 'c', 'd'}],
                    'getY': [{'f', 'g', 'h'}, {'b', 'c', 'd'}, {'e'}]}
        return skeleton, expected

    def test_pi_1(self):
        edge_set = {('a', 'b'), ('a', 'd'), ('b', 'a'), ('d', 't')}

        assert pi_1('a', edge_set) == {('a', 'b'), ('a', 'd')}
        assert pi_1('b', edge_set) == {('b', 'a')}
        assert pi_1('d', edge_set) == {('d', 't')}
        assert pi_1('t', edge_set) == set()

    def test_pi_2(self):
        edge_set = {('a', 'b'), ('a', 'd'), ('b', 'a'), ('d', 't')}

        assert pi_2('a', edge_set) == {('b', 'a')}
        assert pi_2('b', edge_set) == {('a', 'b')}
        assert pi_2('d', edge_set) == {('a', 'd')}
        assert pi_2('t', edge_set) == {('d', 't')}
        assert pi_2('s', edge_set) == set()

    def test_pi_both(self):
        edge_set = {('a', 'b'), ('a', 'd'), ('b', 'a'), ('d', 't')}

        assert pi_both('a', 'b', edge_set, [], []) == {('a', 'b'), ('a', 'd')}
        assert pi_both('b', 'a', edge_set, [], []) == {('b', 'a')}
        assert pi_both('d', 'a', edge_set, [], []) == {('d', 't'), ('b', 'a')}
        assert pi_both('s', 'z', edge_set, [], []) == set()

    def test_ValidCausalPassages(self, validCausal, validCausal2):
        passage_set = algorithm(validCausal[0])
        assert len(passage_set) == 5
        assert len(validCausal[1] | passage_set) == 5

        for passage in validCausal[1]:
            assert passage in passage_set

        for passage in passage_set:
            assert isinstance(passage, Passage)

        passage_set2 = algorithm(validCausal2[0])
        assert len(passage_set2) == 4
        assert len(validCausal2[1] | passage_set2) == 4

        for passage in validCausal2[1]:
            assert passage in passage_set2

        for passage in passage_set2:
            assert isinstance(passage, Passage)

    def test_DiGraphInput(self, validDiGraph):
        exp_getX = validDiGraph[1]['getX']
        exp_getY = validDiGraph[1]['getY']
        passage_set = algorithm(validDiGraph[0])
        assert len(passage_set) == 3
        assert len(passage_set) == len(exp_getX)

        for p in passage_set:
            assert p.digraph_link is not None
            assert isinstance(p, Passage)
            assert p.getX() in exp_getX
            assert p.getY() in exp_getY
