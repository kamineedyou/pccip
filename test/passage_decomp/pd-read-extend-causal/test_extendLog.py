import pytest
import os
from pm4py.objects.log.importer.xes import importer as xes_importer
from pccip.passage_decomp.pd.extendLog import extendEventLog


class Test_ExtendLog:
    @pytest.fixture
    def validEventLog(self):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'figure8.xes')
        return xes_importer.apply(pathToFile)

    def test_ExtendValidLog(self, validEventLog):
        ext_log = extendEventLog(validEventLog)
        # Check if all the traces have both the added activities
        for trace in ext_log:
            assert trace[0]['concept:name'] == 'Artificial:Start'
            assert trace[-1]['concept:name'] == 'Artificial:End'

    def test_ExtendInvalidLog(self):
        # Use String as opposed to EventLog
        with pytest.raises(TypeError):
            extendEventLog("Process Model")
