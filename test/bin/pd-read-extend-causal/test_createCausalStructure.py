import pytest
import os
from pccip.bin.pd.createCausalStructure import generateCausalStructure
from pccip.bin.pd.createCausalStructure import Causal_Struct
from pm4py.objects.log.importer.xes import importer as xes_importer


class Test_CausalStructure:
    @pytest.fixture
    def validEventLog(self):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'figure1.xes')
        return xes_importer.apply(pathToFile)

    def test_ValidLogDefaults(self, validEventLog):
        causal = generateCausalStructure(validEventLog)
        assert isinstance(causal, Causal_Struct)

    def test_ValidLogVariantsParam(self, validEventLog):
        causal = generateCausalStructure(validEventLog, variants='alpha')
        causal2 = generateCausalStructure(validEventLog, variants='heuristic')
        # Show that both variants provide dictionary outputs
        assert isinstance(causal, Causal_Struct)
        assert isinstance(causal2, Causal_Struct)
        # Show that different variants give different outputs
        assert causal != causal2
        # See if the outputs are correct to previously known values
        assert ('a', 'b') in causal.successors
        assert ('b', 'a') in causal.predecessors
        assert ('b', 'd') in causal.parallel
        assert len(causal.parallel) == 4
        assert ('a', 'b') in causal2.successors
        assert ('b', 'a') in causal2.predecessors
        assert len(causal2.parallel) == 0

    def test_InvalidLogDefaults(self):
        # Use String as opposed to EventLog
        with pytest.raises(TypeError):
            generateCausalStructure('Process Model')
