import pytest
from pccip.bin.passages.passage import Passage
from pccip.bin.passages.min_passages import algorithm, pi_1, pi_2


class Test_CausalStructure:
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

    def test_ValidCausalPassages(self, validCausal):
        passage_set = algorithm(validCausal[0])
        assert len(passage_set) == 5
        assert len(validCausal[1] | passage_set) == 5

        for passage in validCausal[1]:
            assert passage in passage_set

        for passage in passage_set:
            assert isinstance(passage, Passage)
