import os
from pccip.passage_decomp.cc.EventLogDecomp import decompose_event_log
from pm4py.objects.log.importer.xes import importer as xes_importer


class Test_EventLogDecomp:

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
