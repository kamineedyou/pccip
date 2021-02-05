from typing import Set, Tuple
from pm4py.objects.log.log import EventLog
from pccip.bin.pd.c_variants import Variants


def create_causal_structure(log: EventLog,
                            variant: Variants = 'DEFAULT_VARIANT',
                            params: dict = None) -> Set[Tuple[str, str]]:
    if not isinstance(log, EventLog):
        raise TypeError('Invalid Log Type')

    variant = getattr(Variants, variant, None)
    if variant is None:
        raise TypeError('Invalid input variant (c_algo)')

    if params is None:
        params = {}

    return variant(log, params)
