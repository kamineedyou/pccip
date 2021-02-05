from pccip.bin.pd.importLog import importEventLog as import_log
from pccip.bin.pd.extendLog import extendEventLog as extend_log
from pccip.bin.pd.createCausalStructure import generateCausalStructure as gcs
from pccip.bin.passages.min_passages import algorithm as min_passages
from pccip.bin.cc.EventLogDecomp import decompose_event_log as log_decomp
from pccip.bin.pd.logToFragments import create_fragment, merge_fragments
from pccip.bin.pd.logToFragments import Variants as pAlgo


def algorithm(xes,
              c_algo: str = 'alpha',
              p_algo: pAlgo = pAlgo.DEFAULT_VARIANT):

    # import event log (through file path or already imported xes)
    log = import_log(xes)

    # extend the event log
    ext_log = extend_log(log)

    # generate causal structure of the event log
    causal = gcs(ext_log, variants=c_algo)

    # generate passages using the causal structure
    passage_set = min_passages(causal.successors)

    # generate sublogs based off of each passage
    sublogs = set()
    for passage in passage_set:
        sublogs.add(log_decomp(ext_log, passage.getTVis()))

    # generate fragment based off of each sublog
    fragments = []
    for sublog in sublogs:
        fragments.append(create_fragment(sublog, variant=p_algo))

    # merge the fragments to create the final petri net
    result_net, result_im, result_fm = merge_fragments(fragments)

    return result_net, result_im, result_fm
