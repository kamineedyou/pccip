import pytest
from pm4py.objects.log.importer.xes import importer as xes_importer
from pccip.bin.pd.extendLog import extendEventLog


class Test_ExtendLog:
    @pytest.fixture
    def validEventLog(self):
        return xes_importer.apply('figure8.xes')

    def test_ExtendValidLog(self, validEventLog):
        ext_log = extendEventLog(validEventLog)
        # Check if all the traces have both the added activities
        for trace in ext_log:
            assert trace[0]['concept:name'] == 'Passage:START'
            assert trace[-1]['concept:name'] == 'Passage:END'

    def test_ExtendInvalidLog(self):
        # Use String as opposed to EventLog
        with pytest.raises(TypeError):
            extendEventLog("Process Model")
