from typing import Tuple, Set, Union
from networkx import DiGraph


class Passage:
    def __init__(self, edges: Union[DiGraph, Set[Tuple[str, str]]] = set(),
                 digraph_link: dict = None):
        if not isinstance(edges, set) and not isinstance(edges, DiGraph):
            raise TypeError('Invalid Input Edges Format.')

        if isinstance(edges, DiGraph) and digraph_link is None:
            self.edges, self.digraph_link = self.digraph_to_tuple(edges)
        else:
            self.edges = edges
            self.digraph_link = digraph_link

    def digraph_to_tuple(self, digraph: DiGraph):
        digraph_link = {}
        tuple_edges = set()
        for edge in digraph.edges:
            src = edge[0]
            tar = edge[1]
            tuple_edges.add((src.name, tar.name))
            digraph_link[(src.name, tar.name)] = edge
            digraph_link[src.name] = src
            digraph_link[tar.name] = tar
        return tuple_edges, digraph_link

    def get_digraph_edge(self, edge: Tuple[str, str]):
        if self.digraph_link is not None \
           and edge in set(self.digraph_link.keys()):
            return self.digraph_link[edge]
        else:
            return None

    def get_digraph_transition(self, transition: str):
        if self.digraph_link is not None \
           and transition in set(self.digraph_link.keys()):
            return self.digraph_link[transition]
        else:
            return None

    def addEdge(self, edge: Tuple[str, str]):
        if not isinstance(edge, tuple) or not len(edge) == 2 or \
           not isinstance(edge[0], str) or not isinstance(edge[1], str):
            raise TypeError('Invalid Input Edge Format.')

        self.edges.add(edge)

    def getX(self) -> Set[str]:
        x_set = set()
        for edge in self.edges:
            x_set.add(edge[0])

        return x_set

    def getY(self) -> Set[str]:
        y_set = set()
        for edge in self.edges:
            y_set.add(edge[1])

        return y_set

    def getBorderX(self) -> Set[str]:
        return {edge[0] for edge in self.edges
                if edge[0] not in {edge2[1] for edge2 in self.edges
                                   if edge2[0] != edge2[1]}}

    def getBorderY(self) -> Set[str]:
        return {edge[1] for edge in self.edges
                if edge[1] not in {edge2[0] for edge2 in self.edges
                                   if edge2[0] != edge2[1]}}

    def getXY(self) -> Tuple[Set[str], Set[str]]:
        x_set = set()
        y_set = set()

        for edge in self.edges:
            x_set.add(edge[0])
            y_set.add(edge[1])

        return x_set, y_set

    def __repr__(self) -> str:
        x = sorted(list(self.getX()))
        y = sorted(list(self.getY()))
        return 'X=' + str(x) + ', Y=' + str(y)

    def __eq__(self, obj) -> bool:
        x = sorted(list(self.getX()))
        y = sorted(list(self.getY()))
        other_x = sorted(list(obj.getX()))
        other_y = sorted(list(obj.getY()))

        if x == other_x and y == other_y:
            return True
        return False

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __add__(self, obj):
        if not isinstance(obj, Passage):
            raise TypeError(type(obj), 'cannot be added to', type(Passage))
        new_edges = self.edges | obj.edges
        if self.digraph_link is not None and obj.digraph_link is not None:
            new_digraph = self.digraph_link | obj.digraph_link
        else:
            new_digraph = None

        return Passage(new_edges, new_digraph)

    def __sub__(self, obj):
        if not isinstance(obj, Passage):
            raise TypeError(
                type(obj), 'cannot be subtracted from', type(Passage))

        new_edges = self.edges - obj.edges
        if self.digraph_link is not None and obj.digraph_link is not None:
            new_digraph = {k: self.digraph_link[k]
                           for k in
                           set(self.digraph_link) - set(obj.digraph_link)}
        else:
            new_digraph = None

        return Passage(new_edges, new_digraph)
