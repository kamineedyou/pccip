from pccip.bin.passages.passage import Passage
from typing import Set, Tuple


def algorithm(edges: Set[Tuple[str, str]], silents: Set[str]) -> Set[Passage]:
    passage_set = set()

    while edges:
        t_vis = set()
        p_prev = set()
        p_curr = set()
        p_new = set()
        p_curr.add(edges.pop())

        while len(p_curr) - len(p_prev):
            p_prev = p_curr

            for match in p_curr:
                x = match[0]
                y = match[1]
                t_vis.update({x, y})
                p_new = pi_both(x, y, edges, silents, t_vis)
                p_curr = p_curr | p_new
            edges = edges - p_curr

        passage_set.add(Passage(p_curr))

    return passage_set


def pi_both(x_activity: str, y_activity: str, edges: Set[Tuple[str, str]],
            silents: Set[str], t_vis: Set[str]) -> Set[Tuple[str, str]]:
    return {edge for edge in edges
            if edge[0] == x_activity
            or edge[1] == y_activity
            or (edge[0] in silents and edge[0] in t_vis)
            or (edge[1] in silents and edge[1] in t_vis)}
