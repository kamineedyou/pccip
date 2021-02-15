from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.log import EventLog
from typing import Union
from copy import deepcopy


def import_log(xes: Union[EventLog, str]) -> EventLog:
    """Import event log from file or return EventLog object if it was used
    as parameter.

    Args:
        xes (Union[EventLog, str]): input file path to xes file. if EventLog
                                    object already present, return it instead.

    Raises:
        TypeError: Raised when xes parameter is not of type str or EventLog.
        TypeError: Raised when the file type in path is not '.xes'.

    Returns:
        EventLog: Imported event log.
    """
    if not isinstance(xes, str) and not isinstance(xes, EventLog):
        raise TypeError("Invalid Event Log Type or Path")

    if isinstance(xes, EventLog):
        return deepcopy(xes)

    if ".xes" not in xes:
        raise TypeError("Log type is not supported")

    return xes_importer.apply(xes)
