from pccip.bin.cc.net_fragments import create_net_fragments
import os
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.alpha.algorithm import apply
from pm4py.objects.petri.importer import importer as pnml_importer
from pm4py.objects.petri.petrinet import PetriNet
from pccip.bin.cc.extendModel import extendModel
from pccip.bin.utils.transformSkeleton import petriNetIntoSkeleton
from pccip.bin.passages.min_passages import algorithm


class TestNnetFragmnets:

    def test_validFragments(self):

        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'figure1.xes')
        log = xes_importer.apply(pathToFile)
        process_model, im, fm = apply(log)
        (extendedNet, extendedInitMarking, extendedFinalMarking) = extendModel(
            process_model, im, fm)
        skeletonGraph = petriNetIntoSkeleton(extendedNet)
        transitionsOfExtendedNet = extendedNet.transitions
        silentTransOfExtended = [
            silentTrans for silentTrans
            in transitionsOfExtendedNet if silentTrans.label is None]
        passages = algorithm(skeletonGraph, silentTransOfExtended)
        fragments_test = create_net_fragments(passages)
        passages = list(passages)
        true = True
        for cnt, fragment_tuple_test in enumerate(fragments_test):
            x, y = passages[cnt].getXY()
            x = list(x)
            if "Artificial:Start" in x:
                idx = x.index("Artificial:Start")
                print(idx)
                x[idx] = "Start"
            x = sorted(x)

            y = list(y)
            if "Artificial:End" in y:
                idx = y.index("Artificial:End")
                print(idx)
                y[idx] = "End"

            y = sorted(y)
            fragment_test, im_test, fm_test = fragment_tuple_test
            filename = "passage_"+str(x)+str(y)+".pnml"
            path = os.path.join(currentDir, filename)
            fragment_valid, im_valid, fm_valid = pnml_importer.apply(path)

            assert str(im_valid) == str(im_test)
            assert str(fm_test) == str(fm_valid)
            for arc in fragment_test.arcs:
                found = False
                if isinstance(arc.source, PetriNet.Place):
                    arc_source_test = "place"
                else:
                    arc_source_test = arc.source.label

                if isinstance(arc.target, PetriNet.Place):
                    arc_sink_test = "place"
                else:
                    arc_sink_test = arc.target.label

                for arc_valid in fragment_valid.arcs:
                    if isinstance(arc_valid.source, PetriNet.Place):
                        arc_source_vaild = "place"
                    else:
                        arc_source_vaild = arc_valid.source.label

                    if isinstance(arc_valid.target, PetriNet.Place):
                        arc_sink_vaild = "place"
                    else:
                        arc_sink_vaild = arc_valid.target.label

                    if arc_source_test == arc_source_vaild:
                        if arc_sink_test == arc_sink_vaild:
                            found = True
                            break
                assert found == true
