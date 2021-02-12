from passage_decomp.passages.passage import Passage, digraph_to_tuple
from networkx import DiGraph
from typing import Set, Tuple, Union


def algorithm(edges: Union[DiGraph, Set[Tuple[str, str]]],
              silents: Set[str] = []) -> Set[Passage]:
    """Algorithm to compute the minimal passages in an edge set or a DiGraph.

    Args:
        edges (Union[DiGraph, Set[Tuple[str, str]]]): Edge set or DiGraph
            object to create minimal passages out of.
        silents (Set[str], optional): Set of silent transitions.
                                      Defaults to [].

    Returns:
        Set[Passage]: Set of all minimal passages contained in the input edges.
    """
    passage_set = set()

    if isinstance(edges, DiGraph):
        edges, digraph_link = digraph_to_tuple(edges)
    else:
        digraph_link = None

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

        passage_set.add(Passage(p_curr, digraph_link))

    return passage_set


def pi_both(x_activity: str, y_activity: str, edges: Set[Tuple[str, str]],
            silents: Set[str], t_vis: Set[str]) -> Set[Tuple[str, str]]:
    """Get all edges that have x_activity as the source and all the edges that
    have y_activity as the target in one for loop. In addition, add all of the
    edges that hold the same silent transition into the same passage.

    Args:
        x_activity (str): Transition label x.
        y_activity (str): Transition albel y.
        edges (Set[Tuple[str, str]]): Remaining edge set to check.
        silents (Set[str]): Set of names of silent transitions in the net.
        t_vis (Set[str]): Set of transitions in the passage.

    Returns:
        Set[Tuple[str, str]]: Edges to add to the current passage.
    """
    return {edge for edge in edges
            if edge[0] == x_activity
            or edge[1] == y_activity
            or (edge[0] in silents and edge[0] in t_vis)
            or (edge[1] in silents and edge[1] in t_vis)}


def pi_1(x_activity: str, edges: Set[Tuple[str, str]]) -> Set[Tuple[str, str]]:
    """Get all edges that have x_activity as the source.

    Args:
        x_activity (str): Transition label.
        edges (Set[Tuple[str, str]]): Remaining edge set to check.

    Returns:
        Set[Tuple[str, str]]: Edges to add to the current passage.
    """
    return {edge for edge in edges if edge[0] == x_activity}


def pi_2(y_activity: str, edges: Set[Tuple[str, str]]) -> Set[Tuple[str, str]]:
    """Get all edges that have y_activity as the target.

    Args:
        y_activity (str): Transition label.
        edges (Set[Tuple[str, str]]): Remaining edge set to check.

    Returns:
        Set[Tuple[str, str]]: Edges to add to the current passage.
    """
    return {edge for edge in edges if edge[1] == y_activity}
