import pytest
import os
import sys
from pm4py.objects.log.util import basic_filter
from pccip.bin.cc.EventLogDecomp import decompose_event_log
from pm4py.objects.log.importer.xes import importer as xes_importer



class Test_EventLogDecomp:

    @pytest.mark.parametrize("array_events",[["a","b"],["a","c","b"]])
    def test_validDecomp(self,array_events):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'test_log.xes')
        log = xes_importer.apply(pathToFile)

        tracefilter_log_pos = basic_filter.filter_log_events_attr(log,array_events,
                                parameters={basic_filter.Parameters.ATTRIBUTE_KEY: "concept:name",
                                basic_filter.Parameters.POSITIVE: True})

        tracefilter_test = decompose_event_log(log,array_events)

        assert len(tracefilter_test) == len(tracefilter_log_pos)

        for case_index, case in enumerate(tracefilter_log_pos):
            for event_index, event in enumerate(case):
                assert event == tracefilter_test[case_index][event_index]


    @pytest.mark.parametrize("array_events",[["a","b"],["a","c","b"]])
    def test_InvalidDecomp(self,array_events):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'test_log.xes')
        log = xes_importer.apply(pathToFile)
        tracefilter_log_pos = basic_filter.filter_log_events_attr( log, array_events,
                                parameters={basic_filter.Parameters.ATTRIBUTE_KEY: "concept:name",
                                basic_filter.Parameters.POSITIVE: True})

        tracefilter_test = decompose_event_log(log,["c"])

        tracefilter_log_pos_event_set = set()
        for case_index, case in enumerate(tracefilter_log_pos):
                for event_index, event in enumerate(case):
                    tracefilter_log_pos_event_set.add(event)

        tracefilter_test_event_set = set()
        for case_index, case in enumerate(tracefilter_test):
                for event_index, event in enumerate(case):
                    tracefilter_test_event_set.add(event)


        assert tracefilter_test_event_set != tracefilter_log_pos_event_set
