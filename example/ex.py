from pm4py.objects.log.importer.xes import importer as xes_importer


def lenghtOfEventLog(log):
    log = xes_importer.apply(log)
    return len(log)
