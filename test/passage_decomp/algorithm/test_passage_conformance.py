from pccip.passage_decomp.cc.import_model import importPetriNet
from pytest import fixture
from os import path
from pm4py.objects.log.importer.xes import importer as log_importer
from pccip.passage_decomp.algorithm.passageConformance import passage_decompose_conformanceChecking


class Test_conformance_passages:
    @fixture
    def alpha_model(self):
        modelPath = "models/alphamodel.pnml"
        currentDir = path.dirname(path.realpath(__file__))
        pathToModel = path.join(currentDir, modelPath)
        logPath = "logs/roadtraffic50traces.xes"
        pathToLog = path.join(currentDir, logPath)

        (net, init, final) = importPetriNet(pathToModel)
        log = log_importer.apply(pathToLog)

        return (net, init, final, log)

    def test_alpha_model(self, alpha_model):
        print("Give Path to PNML Model")
        net = alpha_model[0]
        init_marking = alpha_model[1]
        final_marking = alpha_model[2]
        log = alpha_model[3]
        num = passage_decompose_conformanceChecking(
            net, init_marking, final_marking, log)

        assert num == 1
