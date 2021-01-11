import extendLog as el
import importLog as il
import createCausalStructure as ccs


def passageProcessDiscovery(xes, cAlgo: str = 'alpha'):
    # import event log (through file path or already imported xes)
    log = il.importEventLog(xes)

    # extend the event log
    ext_log = el.extendEventLog(log)

    # generate causal structure of the event log
    causal = ccs.generateCausalStructure(ext_log, variants=cAlgo)

    return causal
