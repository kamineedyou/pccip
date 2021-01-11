import pytest, os
from pccip.bin.pd.createCausalStructure import generateCausalStructure
from pm4py.objects.log.importer.xes import importer as xes_importer


class Test_CausalStructure:
    @pytest.fixture
    def validEventLog(self):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'figure8.xes')
        return xes_importer.apply(pathToFile)

    def test_ValidLogDefaults(self, validEventLog):
        causal = generateCausalStructure(validEventLog)
        assert isinstance(causal, dict)

    def test_ValidLogVariantsParam(self, validEventLog):
        causal = generateCausalStructure(validEventLog, variants='alpha')
        causal2 = generateCausalStructure(validEventLog, variants='heuristic')
        # Show that both variants provide dictionary outputs
        assert isinstance(causal, dict)
        assert isinstance(causal2, dict)
        # Show that different variants give different outputs
        assert causal != causal2
        # See if the outputs are correct to previously known values
        assert dict(causal['dfg'])[('a', 'b')] == 1
        assert causal2[('a', 'b')] == 0.5

    def test_InvalidLogDefaults(self):
        # Use String as opposed to EventLog
        with pytest.raises(TypeError):
            generateCausalStructure('Process Model')
