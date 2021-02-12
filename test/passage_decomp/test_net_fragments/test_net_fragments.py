# from passage_decomp.cc.net_fragments import net_fragments
# import os
# from pm4py.objects.log.importer.xes import importer as xes_importer
# from passage_decomp.passages.passage import Passage
# from pm4py.algo.discovery.alpha.algorithm import apply
# from pm4py.objects.petri.importer import importer as pnml_importer
# from pm4py.objects.petri.petrinet import PetriNet


# class TestNnetFragmnets:
#     pass
# def test_validFragments(self):

#     currentDir = os.path.dirname(os.path.realpath(__file__))
#     pathToFile = os.path.join(currentDir, 'figure1.xes')
#     log = xes_importer.apply(pathToFile)
#     process_model, im, fm = apply(log)
#     passage_list = [Passage({('h', 'sink'), ('g', 'sink')}),
#                     Passage({('d', 'e'), ('c', 'e'), ('b', 'e')}),
#                     Passage({('source', 'a')}),
#                     Passage({('e', 'f'), ('e', 'h'), ('e', 'g')})]

#     net_fragments_test = net_fragments(passage_list, process_model, im, fm)

#     valid_fragments = []
#     filenames = ['test_passage_g_h.pnml']
#     filenames.append("test_passage_d_c_b.pnml")
#     filenames.append("test_passage_source.pnml")
#     filenames.append("test_passage_e.pnml")

#     for filename in filenames:
#         pathToValid = os.path.join(currentDir, filename)
#         fragment, im, fm = pnml_importer.apply(pathToValid)
#         fragment = tuple([fragment, im, fm])
#         valid_fragments.append(fragment)

#     for cnt, valid_fragment in enumerate(valid_fragments):
#         true = True
#         valid_net, valid_im, valid_fm = valid_fragment
#         test_net, test_im, test_fm = net_fragments_test[cnt]

#         assert str(valid_im) == str(test_im)
#         assert str(valid_fm) == str(test_fm)
#         for arc in test_net.arcs:
#             found = False
#             if isinstance(arc.source, PetriNet.Place):
#                 arc_source_test = "place"
#             else:
#                 arc_source_test = arc.source.label

#             if isinstance(arc.target, PetriNet.Place):
#                 arc_sink_test = "place"
#             else:
#                 arc_sink_test = arc.target.label

#             for arc_valid in valid_net.arcs:
#                 if isinstance(arc_valid.source, PetriNet.Place):
#                     arc_source_vaild = "place"
#                 else:
#                     arc_source_vaild = arc_valid.source.label

#                 if isinstance(arc_valid.target, PetriNet.Place):
#                     arc_sink_vaild = "place"
#                 else:
#                     arc_sink_vaild = arc_valid.target.label

#                 if arc_source_test == arc_source_vaild:
#                     if arc_sink_test == arc_sink_vaild:
#                         found = True
#                         break
#             assert found == true
