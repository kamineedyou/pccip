import pytest
import os
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.log import EventLog, Trace
from pccip.bin.pd.logToFragments import split_log


class Test_SplitLog:
    @pytest.fixture
    def parallelSplit(self):
        file_list = ['bcde.xes']
        sublog_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'logs/' + f)
            sublog_list.append(xes_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'logs/bcdeSPLIT.xes')
        expected = xes_importer.apply(pathToFile)
        return sublog_list, expected

    @pytest.fixture
    def startLoopSplit(self):
        file_list = ['abcdf.xes']
        sublog_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'logs/' + f)
            sublog_list.append(xes_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'logs/abcdfSPLIT.xes')
        expected = xes_importer.apply(pathToFile)
        return sublog_list, expected

    @pytest.fixture
    def endLoopSplit(self):
        file_list = ['efgh.xes']
        sublog_list = []
        currentDir = os.path.dirname(os.path.realpath(__file__))
        for f in file_list:
            pathToFile = os.path.join(currentDir, 'logs/' + f)
            sublog_list.append(xes_importer.apply(pathToFile))

        pathToFile = os.path.join(currentDir, 'logs/efghSPLIT.xes')
        expected = xes_importer.apply(pathToFile)
        return sublog_list, expected

    # sublog contains parallel activities at passage X set
    def test_SplitWithParallel(self, parallelSplit):
        sublog = parallelSplit[0][0]
        expected_split = parallelSplit[1]
        expected_traces = []
        # generate list of activities in each trace in order
        for trace in expected_split:
            expected_traces.append([x['concept:name'] for x in trace])
        # use split_log function
        new_split = split_log(sublog)
        assert isinstance(new_split, EventLog)
        assert len(new_split._list) == len(expected_split._list)

        # check if the traces are the same as expected
        for trace in new_split:
            calc_trace = [x['concept:name'] for x in trace]
            assert calc_trace in expected_traces

    # sublog contains parallel activities at passage X set
    def test_SplitWithLoopAtStart(self, startLoopSplit):
        sublog = startLoopSplit[0][0]
        expected_split = startLoopSplit[1]
        expected_traces = []
        # generate list of activities in each trace in order
        for trace in expected_split:
            expected_traces.append([x['concept:name'] for x in trace])
        # use split_log function
        new_split = split_log(sublog)
        assert isinstance(new_split, EventLog)
        assert len(new_split._list) == len(expected_split._list)

        # check if the traces are the same as expected
        for trace in new_split:
            assert isinstance(trace, Trace)
            calc_trace = [x['concept:name'] for x in trace]
            assert calc_trace in expected_traces

    # sublog contains parallel activities at passage X set
    def test_SplitWithLoopAtEnd(self, endLoopSplit):
        sublog = endLoopSplit[0][0]
        expected_split = endLoopSplit[1]
        expected_traces = []
        # generate list of activities in each trace in order
        for trace in expected_split:
            assert isinstance(trace, Trace)
            expected_traces.append([x['concept:name'] for x in trace])
        # use split_log function
        new_split = split_log(sublog)
        assert isinstance(new_split, EventLog)
        assert len(new_split._list) == len(expected_split._list)

        # check if the traces are the same as expected
        for trace in new_split:
            assert isinstance(trace, Trace)
            calc_trace = [x['concept:name'] for x in trace]
            assert calc_trace in expected_traces

    def test_InvalidInput(self):
        with pytest.raises(TypeError):
            split_log('<xml>event log</xml>')
            split_log(Trace())
