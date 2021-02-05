import pytest
import os
from pccip.bin.pd.createCausalStructure import create_causal_structure
from pm4py.objects.log.importer.xes import importer as xes_importer


class Test_CausalStructure:
    @pytest.fixture
    def validEventLog(self):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'figure1.xes')
        return xes_importer.apply(pathToFile)

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
