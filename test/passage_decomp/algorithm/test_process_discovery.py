import pytest
import os
from pm4py.objects.petri.importer import importer as pnml_importer
from pm4py.objects.log.importer.xes import importer as log_importer
from pm4py.objects.petri.petrinet import PetriNet, Marking
from passage_decomp.algorithm.process_discovery import passage_process_discovery
from pm4py.algo.discovery.footprints.algorithm import apply as footprints


class Test_Process_Discovery:

    @pytest.fixture
    def alpha_figure_1(self):
        file_name = 'figure1.xes'
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'logs/' + file_name)
        result = log_importer.apply(pathToFile)

        file_path = os.path.join(currentDir, 'models/figure1_palpha.pnml')
        expected = pnml_importer.apply(file_path)

        file_path = os.path.join(currentDir, 'models/figure1_alpha.pnml')
        expected_normal = pnml_importer.apply(file_path)

        return result, expected, expected_normal

    @pytest.fixture
    def alpha_figure_1_no_end_xor(self):
        file_name = 'figure1.xes'
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'logs/' + file_name)
        result = log_importer.apply(pathToFile)

        file_path = os.path.join(currentDir,
                                 'models/figure1_remove_last_xor.pnml')
        expected = pnml_importer.apply(file_path)

        c_custom = {('a', 'b'), ('a', 'c'), ('d', 'e'), ('a', 'd'),
                    ('e', 'f'), ('b', 'e'), ('c', 'e'), ('f', 'b'),
                    ('f', 'c'), ('f', 'd')}

        return result, expected, c_custom

    @pytest.fixture
    def inductive_figure_1(self):
        file_name = 'figure1.xes'
        currentDir = os.path.dirname(os.path.realpath(__file__))
        pathToFile = os.path.join(currentDir, 'logs/' + file_name)
        result = log_importer.apply(pathToFile)

        file_path = os.path.join(currentDir, 'models/figure1_pinductive.pnml')
        expected = pnml_importer.apply(file_path)

        file_path = os.path.join(currentDir, 'models/figure1_inductive.pnml')
        expected_normal = pnml_importer.apply(file_path)

        return result, expected, expected_normal

    def test_alpha_figure_1(self, alpha_figure_1):
        test_log = alpha_figure_1[0]
        # expected from the algorithm
        exp_pnet, exp_pim, exp_pfm = alpha_figure_1[1]
        exp_pfoot = footprints(exp_pnet, exp_pim)

        # check return types
        new_net, new_im, new_fm = passage_process_discovery(test_log,
                                                            p_algo='ALPHA')
        new_foot = footprints(new_net, new_im)
        assert isinstance(new_net, PetriNet)
        assert isinstance(new_im, Marking)
        assert isinstance(new_fm, Marking)

        assert new_foot == exp_pfoot

    def test_inductive_figure_1(self, inductive_figure_1):
        test_log = inductive_figure_1[0]
        # expected from the algorithm
        exp_pnet, exp_pim, exp_pfm = inductive_figure_1[1]
        exp_pfoot = footprints(exp_pnet, exp_pim)

        # check return types
        new_net, new_im, new_fm = passage_process_discovery(test_log,
                                                            p_algo='INDUCTIVE')
        new_foot = footprints(new_net, new_im)
        assert isinstance(new_net, PetriNet)
        assert isinstance(new_im, Marking)
        assert isinstance(new_fm, Marking)

        assert new_foot == exp_pfoot

    def test_alpha_figure_1_custom(self, alpha_figure_1_no_end_xor):
        test_log = alpha_figure_1_no_end_xor[0]
        c_custom = alpha_figure_1_no_end_xor[2]
        # expected from the algorithm
        exp_pnet, exp_pim, exp_pfm = alpha_figure_1_no_end_xor[1]
        exp_pfoot = footprints(exp_pnet, exp_pim)

        # check return types
        new_net, new_im, new_fm = passage_process_discovery(test_log,
                                                            p_algo='ALPHA',
                                                            c_custom=c_custom)

        assert isinstance(new_net, PetriNet)
        assert isinstance(new_im, Marking)
        assert isinstance(new_fm, Marking)

        new_foot = footprints(new_net, new_im)
        assert new_foot == exp_pfoot
