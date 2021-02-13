import pytest
import os
from pccip.passage_decomp.pd.causal_structure import create_causal_structure
from pccip.passage_decomp.pd.causal_structure import create_custom_causal_structure
from pccip.passage_decomp.algorithm.constants import ARTIFICIAL_START, ARTIFICIAL_END
from pm4py.objects.log.importer.xes import importer as xes_importer


class Test_CausalStructure:
    @pytest.fixture
    def validEventLog(self):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'figure1.xes')
        return xes_importer.apply(pathToFile)

    @pytest.fixture
    def valid_custom_causal(self):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'figure1.xes')
        input_log = xes_importer.apply(pathToFile)
        input_edges = {('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'e'),
                       ('c', 'e'), ('d', 'e'), ('e', 'f'), ('f', 'b'),
                       ('f', 'c'), ('f', 'd'), ('e', 'g'), ('e', 'h')}
        expected_edges = {(ARTIFICIAL_START, 'a'), ('a', 'b'), ('a', 'c'),
                          ('a', 'd'), ('b', 'e'), ('c', 'e'), ('d', 'e'),
                          ('e', 'f'), ('f', 'b'), ('f', 'c'), ('f', 'd'),
                          ('e', 'g'), ('e', 'h'), ('g', ARTIFICIAL_END),
                          ('h', ARTIFICIAL_END)}

        return input_edges, expected_edges, input_log

    def test_ValidLogDefaults(self, validEventLog):
        causal = create_causal_structure(validEventLog)
        assert isinstance(causal, set)

    def test_ValidLogVariantsParam(self, validEventLog):
        causal = create_causal_structure(validEventLog, variant='ALPHA')
        causal2 = create_causal_structure(validEventLog, variant='HEURISTIC')
        # Show that both variants provide dictionary outputs
        assert isinstance(causal, set)
        assert isinstance(causal2, set)
        # Show that different variants give different outputs
        assert causal == causal2
        # See if the outputs are correct to previously known values
        assert len(causal) == len(causal2)
        assert ('a', 'b') in causal
        assert ('c', 'e') in causal
        assert ('f', 'c') in causal
        assert ('a', 'b') in causal2
        assert ('b', 'e') in causal2

        causal3 = create_causal_structure(validEventLog,
                                          variant='HEURISTIC',
                                          params={'threshold': 0.7})

        assert causal != causal3

    def test_InvalidLogDefaults(self):
        # Use String as opposed to EventLog
        with pytest.raises(TypeError):
            create_causal_structure('Process Model')

    def test_InvalidCausalVariant(self, validEventLog):
        # Use String as opposed to EventLog
        with pytest.raises(TypeError):
            create_causal_structure(validEventLog, variants='fake-variant')

    def test_valid_custom_structure(self, valid_custom_causal):
        input_edges = valid_custom_causal[0]
        expected = valid_custom_causal[1]
        input_log = valid_custom_causal[2]

        test_edges = create_custom_causal_structure(input_edges, input_log)
        # testing the extending of the edges
        assert len(test_edges) == len(expected)
        assert test_edges == expected
