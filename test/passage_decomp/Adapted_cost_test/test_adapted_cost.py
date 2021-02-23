import os
import pytest
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.petri.importer import importer as pnml_importer
from pccip.passage_decomp.cc import adapted_cost


@pytest.mark.parametrize(('tupl, result'),
                         [(('a', 'b'), None),
                         (('a', '>>'), 'a'),
                         (('a', None), None)])
def test_Get_Acti(tupl, result):
    assert adapted_cost.contains_skip(tupl) == result


@pytest.fixture
def figure1_perfect():
    pwd_path = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(pwd_path, 'figure1.xes')
    log = xes_importer.apply(log_path)

    whole_model_path = os.path.join(pwd_path, 'figure1.pnml')
    whole_model = pnml_importer.apply(whole_model_path)

    fragments = []
    for i in range(5):
        fragment_path = os.path.join(pwd_path, f'fragment{i}.pnml')
        fragments.append(pnml_importer.apply(fragment_path))

    return log, fragments, whole_model


@pytest.fixture
def figure1_many_small_trace_problems():
    pwd_path = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(pwd_path, 'figure1_bad.xes')
    log = xes_importer.apply(log_path)

    whole_model_path = os.path.join(pwd_path, 'figure1.pnml')
    whole_model = pnml_importer.apply(whole_model_path)

    fragments = []
    for i in range(5):
        fragment_path = os.path.join(pwd_path, f'fragment{i}.pnml')
        fragments.append(pnml_importer.apply(fragment_path))

    return log, fragments, whole_model


@pytest.fixture
def figure1_only_one_bad_trace_36times():
    pwd_path = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(pwd_path, 'figure1_one_bad_trace.xes')
    log = xes_importer.apply(log_path)

    whole_model_path = os.path.join(pwd_path, 'figure1.pnml')
    whole_model = pnml_importer.apply(whole_model_path)

    fragments = []
    for i in range(5):
        fragment_path = os.path.join(pwd_path, f'fragment{i}.pnml')
        fragments.append(pnml_importer.apply(fragment_path))

    return log, fragments, whole_model


@pytest.fixture
def figure1_completely_different_event_log():
    pwd_path = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(pwd_path, 'roadtraffic50traces.xes')
    log = xes_importer.apply(log_path)

    whole_model_path = os.path.join(pwd_path, 'figure1.pnml')
    whole_model = pnml_importer.apply(whole_model_path)

    fragments = []
    for i in range(5):
        fragment_path = os.path.join(pwd_path, f'fragment{i}.pnml')
        fragments.append(pnml_importer.apply(fragment_path))

    return log, fragments, whole_model


@pytest.fixture
def figure1_inductive_bad():
    pwd_path = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(pwd_path, 'figure1_bad.xes')
    log = xes_importer.apply(log_path)

    whole_model_path = os.path.join(pwd_path, 'figure1.pnml')
    whole_model = pnml_importer.apply(whole_model_path)

    fragments = []
    for i in range(5):
        fragment_path = os.path.join(pwd_path, f'fragment{i}_inductive.pnml')
        fragments.append(pnml_importer.apply(fragment_path))

    return log, fragments, whole_model


def test_perfect_log(figure1_perfect):
    log = figure1_perfect[0]
    fragments = figure1_perfect[1]
    model = figure1_perfect[2]

    local_align = adapted_cost.passage_alignment(fragments, log)
    assert len(local_align) == 5

    # alignment denominator
    trace_count = len(log)
    event_dict = adapted_cost.get_event_count(log)
    event_number = sum(event_dict.values())
    best_worst_cost = adapted_cost.get_minimum_distance(model[0],
                                                        model[1],
                                                        model[2])
    alignment_denominator = adapted_cost.alignments_denominator(trace_count,
                                                                event_number,
                                                                best_worst_cost)
    assert alignment_denominator == 116

    # alignment numerator
    empty_trace_number = adapted_cost.entire_trace_gone_number(local_align)
    align_cost_sum = adapted_cost.sum_costs(local_align)
    missing_labels = adapted_cost.account_missing_labels(local_align,
                                                         event_dict)
    empty_trace_cost = best_worst_cost * empty_trace_number
    alignment_numerator = align_cost_sum + missing_labels + empty_trace_cost

    assert align_cost_sum == 0
    assert alignment_numerator == 0

    # global check
    global_align = adapted_cost.get_global_fitness(local_align, log,
                                                   best_worst_cost)
    assert global_align['fitness'] == 1.0
    assert global_align['percFitTraces'] == 1.0


def test_many_small_log_problems(figure1_many_small_trace_problems):
    log = figure1_many_small_trace_problems[0]
    fragments = figure1_many_small_trace_problems[1]
    model = figure1_many_small_trace_problems[2]

    local_align = adapted_cost.passage_alignment(fragments, log)
    assert len(local_align) == 5

    # alignment denominator
    trace_count = len(log)
    event_dict = adapted_cost.get_event_count(log)
    event_number = sum(event_dict.values())
    best_worst_cost = adapted_cost.get_minimum_distance(model[0],
                                                        model[1],
                                                        model[2])
    alignment_denominator = adapted_cost.alignments_denominator(trace_count,
                                                                event_number,
                                                                best_worst_cost)
    assert alignment_denominator == 137

    # alignment numerator
    empty_trace_number = adapted_cost.entire_trace_gone_number(local_align)
    align_cost_sum = adapted_cost.sum_costs(local_align)
    missing_labels = adapted_cost.account_missing_labels(local_align,
                                                         event_dict)
    empty_trace_cost = best_worst_cost * empty_trace_number
    alignment_numerator = align_cost_sum + missing_labels + empty_trace_cost

    assert align_cost_sum == 11.5
    assert alignment_numerator == 11.5

    # global check
    global_align = adapted_cost.get_global_fitness(local_align, log,
                                                   best_worst_cost)
    assert global_align['fitness'] == 0.916058394160584
    assert global_align['percFitTraces'] == 0.7272727272727273


def test_log_one_bad_trace_36times(figure1_only_one_bad_trace_36times):
    log = figure1_only_one_bad_trace_36times[0]
    fragments = figure1_only_one_bad_trace_36times[1]
    model = figure1_only_one_bad_trace_36times[2]

    local_align = adapted_cost.passage_alignment(fragments, log)
    assert len(local_align) == 5

    # alignment denominator
    trace_count = len(log)
    event_dict = adapted_cost.get_event_count(log)
    event_number = sum(event_dict.values())
    best_worst_cost = adapted_cost.get_minimum_distance(model[0],
                                                        model[1],
                                                        model[2])
    alignment_denominator = adapted_cost.alignments_denominator(trace_count,
                                                                event_number,
                                                                best_worst_cost)
    assert alignment_denominator == 684

    # alignment numerator
    empty_trace_number = adapted_cost.entire_trace_gone_number(local_align)
    align_cost_sum = adapted_cost.sum_costs(local_align)
    missing_labels = adapted_cost.account_missing_labels(local_align,
                                                         event_dict)
    empty_trace_cost = best_worst_cost * empty_trace_number
    alignment_numerator = align_cost_sum + missing_labels + empty_trace_cost

    assert align_cost_sum == 324
    assert alignment_numerator == 324

    # global check
    global_align = adapted_cost.get_global_fitness(local_align, log,
                                                   best_worst_cost)
    assert global_align['fitness'] == 0.5263157894736843
    assert global_align['percFitTraces'] == 0.0


def test_completely_different_log(figure1_completely_different_event_log):
    log = figure1_completely_different_event_log[0]
    fragments = figure1_completely_different_event_log[1]
    model = figure1_completely_different_event_log[2]

    local_align = adapted_cost.passage_alignment(fragments, log)
    assert len(local_align) == 5

    # alignment denominator
    trace_count = len(log)
    event_dict = adapted_cost.get_event_count(log)
    event_number = sum(event_dict.values())
    best_worst_cost = adapted_cost.get_minimum_distance(model[0],
                                                        model[1],
                                                        model[2])
    alignment_denominator = adapted_cost.alignments_denominator(trace_count,
                                                                event_number,
                                                                best_worst_cost)
    assert alignment_denominator == 456

    # alignment numerator
    empty_trace_number = adapted_cost.entire_trace_gone_number(local_align)
    align_cost_sum = adapted_cost.sum_costs(local_align)
    missing_labels = adapted_cost.account_missing_labels(local_align,
                                                         event_dict)
    empty_trace_cost = best_worst_cost * empty_trace_number
    alignment_numerator = align_cost_sum + missing_labels + empty_trace_cost

    assert align_cost_sum == 0
    assert alignment_numerator == 456

    # global check
    global_align = adapted_cost.get_global_fitness(local_align, log,
                                                   best_worst_cost)
    assert global_align['fitness'] == 0.0
    assert global_align['percFitTraces'] == 0.0


def test_inductive_bad(figure1_inductive_bad):
    log = figure1_inductive_bad[0]
    fragments = figure1_inductive_bad[1]
    model = figure1_inductive_bad[2]

    local_align = adapted_cost.passage_alignment(fragments, log)
    assert len(local_align) == 5

    # alignment denominator
    trace_count = len(log)
    event_dict = adapted_cost.get_event_count(log)
    event_number = sum(event_dict.values())
    best_worst_cost = adapted_cost.get_minimum_distance(model[0],
                                                        model[1],
                                                        model[2])
    alignment_denominator = adapted_cost.alignments_denominator(trace_count,
                                                                event_number,
                                                                best_worst_cost)
    assert alignment_denominator == 137

    # alignment numerator
    empty_trace_number = adapted_cost.entire_trace_gone_number(local_align)
    align_cost_sum = adapted_cost.sum_costs(local_align)
    missing_labels = adapted_cost.account_missing_labels(local_align,
                                                         event_dict)
    empty_trace_cost = best_worst_cost * empty_trace_number
    alignment_numerator = align_cost_sum + missing_labels + empty_trace_cost

    assert align_cost_sum == 11.5
    assert alignment_numerator == 11.5

    # global check
    global_align = adapted_cost.get_global_fitness(local_align, log,
                                                   best_worst_cost)
    assert global_align['fitness'] == 0.916058394160584
    assert global_align['percFitTraces'] == 0.7272727272727273
