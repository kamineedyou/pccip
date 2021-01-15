import datetime
from pm4py.objects.log.log import Event, EventLog


def generateStartEvent() -> Event:
    start = {'concept:name': 'Artificial:Start',
             'lifecycle:transition': 'complete',
             'time:timestamp':
                 datetime.datetime(1, 1, 1, 0, 0,
                                   tzinfo=datetime.timezone(
                                       datetime.timedelta(seconds=3600)))
             }

    return Event(start)


def generateEndEvent() -> Event:
    end = {'concept:name': 'Artificial:End',
           'lifecycle:transition': 'complete',
           'time:timestamp':
               datetime.datetime(9999, 12, 31, 0, 0,
                                 tzinfo=datetime.timezone(
                                     datetime.timedelta(seconds=3600)))
           }

    return Event(end)


def extendEventLog(log: EventLog) -> EventLog:
    if not isinstance(log, EventLog):
        raise TypeError("Invalid log type")

    start = generateStartEvent()
    end = generateEndEvent()
    for trace in log:
        trace.insert(0, start)
        trace.append(end)

    return log
