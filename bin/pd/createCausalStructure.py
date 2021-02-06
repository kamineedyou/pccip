from typing import Set, Tuple
from pm4py.objects.log.log import EventLog
from pccip.bin.pd.c_variants import Variants


def create_causal_structure(log: EventLog,
                            variant: str = 'DEFAULT_VARIANT',
                            params: dict = None) -> Set[Tuple[str, str]]:
    """Generate the causal structure (sequence edges) from an event log.

    Args:
        log (EventLog): Event log to create a causal structure from.
        variant (str, optional): Causal algorithm variant to create a
                                 causal structure.
                                 Variants available: 'ALPHA', 'HEURISTIC'.
                                 Defaults to 'DEFAULT_VARIANT'.
        params (dict, optional): Parameters for the discovery algorithm.
                                 Defaults to None.

    Raises:
        TypeError: Raised when input is not of type EventLog.
        TypeError: Raised when the variant is invalid.

    Returns:
        Set[Tuple[str, str]]: Sequence edges from the entire event log.
    """
    if not isinstance(log, EventLog):
        raise TypeError('Invalid Log Type')

    variant = getattr(Variants, variant.upper(), None)
    if variant is None:
        raise TypeError('Invalid input variant (c_algo)')

    if params is None:
        params = {}

    return variant(log, params)
