from pytest import fixture
import pm4py
from os import path
from pm4py.objects.log.importer.xes import importer as log_importer
from pccip.passage_decomp.algorithm.conformance_checking import passage_conformance_checking


class Test_conformance_passages:
    @fixture
    def inductive_perfect(self):
        currentDir = path.dirname(path.realpath(__file__))
        logPath = "logs/roadtraffic50traces.xes"
        pathToLog = path.join(currentDir, logPath)
        log = log_importer.apply(pathToLog)
        net, init, final = pm4py.discover_petri_net_inductive(log)

        return net, init, final, log

    @fixture
    def inductive_not_perfect(self):
        currentDir = path.dirname(path.realpath(__file__))
        logPath = "logs/roadtraffic50traces.xes"
        pathToLog = path.join(currentDir, logPath)

        # net, init, final = import_petri_net(pathToModel)
        log = log_importer.apply(pathToLog)
        net, init, final = pm4py.discover_petri_net_inductive(log, 0.2)

        return net, init, final, log

    def test_inductive_perfect(self, inductive_perfect):
        net, init_marking, final_marking = inductive_perfect[:3]
        log = inductive_perfect[3]
        local_align, global_fitness = passage_conformance_checking(
            log, net, init_marking, final_marking)

        assert global_fitness['fitness'] == 1.0
        assert global_fitness['percFitTraces'] == 1.0
        assert len(local_align) == 2

        for f in local_align:
            assert sum(local_align[f]['costs'].values()) == 0

    def test_inductive_not_perfect(self, inductive_not_perfect):
        net, init_marking, final_marking = inductive_not_perfect[:3]
        log = inductive_not_perfect[3]
        local_align, global_fitness = passage_conformance_checking(
            log, net, init_marking, final_marking)

        assert global_fitness['fitness'] == 0.976897689768977
        assert global_fitness['percFitTraces'] == 0.8627450980392157
        assert len(local_align) == 2

        total_cost = 0
        for f in local_align:
            total_cost += sum(local_align[f]['costs'].values())

        assert total_cost == 7
