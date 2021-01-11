from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.log import EventLog


class WrongEventLogType(Exception):
    pass


def importEventLog(xes) -> EventLog:
    if not isinstance(xes, str) and not isinstance(xes, EventLog):
        raise TypeError("Invalid Event Log Type or Path")

    if isinstance(xes, EventLog):
        return xes

    if ".xes" not in xes:
        raise WrongEventLogType("Log type is not supported")

    return xes_importer.apply(xes)
