from pccip.passage_decomp.cc.import_model import import_petri_net, WrongPetriNetModelType
import os
import pytest


class TestImportPetrinet:
    @pytest.mark.parametrize("filePath", ["testModelPNML.pnml"])
    def test_ImportPetriNet(self, filePath):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, filePath)
        (net, initial_marking, final_marking) = import_petri_net(pathToFile)

    @pytest.mark.parametrize("filePath", ["testModelPNML.cpn"])
    def test_ImportWrongPetriNet(self, filePath):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, filePath)
        with pytest.raises(WrongPetriNetModelType):
            (net, initial_marking, final_marking) = import_petri_net(pathToFile)

    @pytest.mark.parametrize("filePath", ["blabla.pmnl"])
    def test_WrongPath(self, filePath):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, filePath)
        with pytest.raises(Exception):
            (net, initial_marking, final_marking) = import_petri_net(pathToFile)
