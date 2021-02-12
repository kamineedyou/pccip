import pytest
import os
from pccip.passage_decomp.pd.import_log import import_log
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.log import EventLog


class Test_ImportLog:
    @pytest.fixture
    def validEventLog(self):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'figure8.xes')
        return xes_importer.apply(pathToFile)

    @pytest.mark.parametrize('filePath', ['figure8.xes'])
    def test_ImportEventLogXESFile(self, filePath):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, filePath)
        xes = import_log(pathToFile)
        assert isinstance(xes, EventLog)

    def test_ImportEventLogPython(self, validEventLog):
        xes = import_log(validEventLog)
        assert isinstance(xes, EventLog)

    @pytest.mark.parametrize('invalidEventLogFileType', ['figure2.txt'])
    def test_ImportInvalidEventLog(self, invalidEventLogFileType):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, invalidEventLogFileType)
        with pytest.raises(TypeError):
            import_log(pathToFile)

    @pytest.mark.parametrize('nonExistantFile', ['figureLOST.xes'])
    def test_ImportNonExistantFile(self, nonExistantFile):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, nonExistantFile)
        with pytest.raises(FileNotFoundError):
            import_log(pathToFile)
