from pccip.bin.passages.passage import Passage
from typing import Set, Tuple


def algorithm(edges: Set[Tuple[str, str]]) -> Set[Passage]:
    passage_set = set()

    while edges:
        p_prev = set()
        p_curr = set()
        p_curr.add(edges.pop())

        while p_curr - p_prev:
            p_prev = p_curr

            for match in p_curr:
                x = match[0]
                y = match[1]

                p_curr = p_curr | pi_1(x, edges) | pi_2(y, edges)
            edges = edges - p_curr

        passage_set.add(Passage(p_curr))

    return passage_set


def pi_1(x_activity: str, edges: Set[Tuple[str, str]]) -> Set[Tuple[str, str]]:
    return {edge for edge in edges if edge[0] == x_activity}


def pi_2(y_activity: str, edges: Set[Tuple[str, str]]) -> Set[Tuple[str, str]]:
    return {edge for edge in edges if edge[1] == y_activity}
