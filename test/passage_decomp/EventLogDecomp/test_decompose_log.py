import os
import pytest
from pccip.passage_decomp.cc.log_decomp import decompose_event_log, efficient_log_decomp
from pm4py.objects.log.importer.xes import importer as xes_importer
from pccip.passage_decomp.passages.min_passages import min_passages
from pccip.passage_decomp.pd.causal_structure import create_causal_structure


class Test_EventLogDecomp:

    @pytest.fixture
    def road_log(self):
        file_name = 'roadtraffic50traces.xes'
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, file_name)
        result = xes_importer.apply(pathToFile)

        causal = create_causal_structure(result, 'alpha')
        passage_set = min_passages(causal)

        return result, passage_set

    def test_validDecomp(self):
        events = ["a", "c", "b"]
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'test_log.xes')
        log = xes_importer.apply(pathToFile)

        pathToFileFilter = os.path.join(currentDir, 'filtered_log_test.xes')
        valid_log = xes_importer.apply(pathToFileFilter)
        filter_test = decompose_event_log(log, events)
        for case_index, case in enumerate(valid_log):
            for event_index, event in enumerate(case):
                assert event == filter_test[case_index][event_index]

    def test_efficient_decomp(self, road_log):
        log = road_log[0]
        passages = road_log[1]

        sublogs_old = set()
        for p in passages:
            sublogs_old.add(decompose_event_log(log, p.getTVis()))

        sublogs_new = efficient_log_decomp(log, passages)

        assert len(sublogs_old) == len(sublogs_new)
        trace_old = set()
        trace_new = set()
        for log in sublogs_new:
            for trace in log:
                trace_new.add(str([x['concept:name'] for x in trace]))

        for log in sublogs_old:
            for trace in log:
                trace_old.add(str([x['concept:name'] for x in trace]))

        assert len(trace_new) == len(trace_old)
        for t in trace_new:
            assert t in trace_old
        for t in trace_old:
            assert t in trace_new
