import pytest
from pccip.bin.NnetFragments.netFragments import net_fragments
import os
from pm4py.objects.log.importer.xes import importer as xes_importer
from pccip.bin.passages.passage import Passage
from pm4py.algo.discovery.alpha.algorithm import apply
from pm4py.objects.petri.importer import importer as pnml_importer


class TestNnetFragmnets:

    def test_validFragments(self):

        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'figure1.xes')
        log = xes_importer.apply(pathToFile)
        process_model, initial_marking, final_marking = apply(log)
        passage_list = [Passage({('h', 'sink'), ('g', 'sink')})]

        NnetFragments_test = net_fragments(passage_list, process_model)
        pathToValidFile = os.path.join(currentDir, 'test_petrinet_passage_g_h.pnml')
        valid_fragments, initial_marking, final_marking = pnml_importer.apply(pathToValidFile)

        valid_trans = valid_fragments.transitions
        test_trans = NnetFragments_test[0].transitions

        assert len(valid_trans) == len(test_trans)

        for arc in NnetFragments_test[0].arcs:
            arc_source_test = arc.source.label
            arc_sink_test = arc.target.name
            found = False
            for arc in valid_fragments.arcs:
                if arc_source_test == arc.source.label and arc_sink_test == arc.target.name:
                    found = True
                    break
            assert found == True
