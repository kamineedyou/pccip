import pytest
from pccip.bin.pd.importLog import importEventLog, WrongEventLogType
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.log import EventLog


class Test_ImportLog:
    @pytest.fixture
    def validEventLog(self):
        return xes_importer.apply('figure8.xes')

    @pytest.mark.parametrize('filePath', ['figure8.xes'])
    def test_ImportEventLogXESFile(self, filePath):
        xes = importEventLog(filePath)
        assert isinstance(xes, EventLog)

    def test_ImportEventLogPython(self, validEventLog):
        xes = importEventLog(validEventLog)
        assert isinstance(xes, EventLog)

    @pytest.mark.parametrize('invalidEventLogFileType', ['figure2.txt'])
    def test_ImportInvalidEventLog(self, invalidEventLogFileType):
        with pytest.raises(WrongEventLogType):
            importEventLog(invalidEventLogFileType)

    @pytest.mark.parametrize('nonExistantFile', ['figureLOST.xes'])
    def test_ImportNonExistantFile(self, nonExistantFile):
        with pytest.raises(FileNotFoundError):
            importEventLog(nonExistantFile)
