from bin.algorithm.passageConformance import passage_decompose_conformanceChecking
from bin.cc.importModel import importPetriNet
from pm4py.objects.log.importer.xes import importer as xes_importer

print("Give Path to PNML Model")
(net, initMarking, finalMarking) = importPetriNet("alphamodel.pnml")
log = xes_importer.apply('roadtraffic50traces.xes')
print(initMarking, finalMarking)
num = passage_decompose_conformanceChecking(
    net, initMarking, finalMarking, log)
print(num)
