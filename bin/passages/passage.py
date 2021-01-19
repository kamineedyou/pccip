from typing import Tuple, Set


class Passage:
    def __init__(self, edges: Set[Tuple[str, str]] = set()):
        if not isinstance(edges, set):
            raise TypeError('Invalid Input Edges Format.')

        self.edges = edges

    def addEdge(self, edge: Tuple[str, str]):
        if not isinstance(edge, tuple) or not len(edge) == 2 or \
           not isinstance(edge[0], str) or not isinstance(edge[1], str):
            raise TypeError('Invalid Input Edge Format.')

        self.edges.add(edge)

    def getX(self) -> Set[Tuple[str, str]]:
        x_set = set()
        for edge in self.edges:
            x_set.add(edge[0])

        return x_set

    def getY(self) -> Set[Tuple[str, str]]:
        y_set = set()
        for edge in self.edges:
            y_set.add(edge[1])

        return y_set

    def getXY(self) -> Tuple[Set[str], Set[str]]:
        x_set = set()
        y_set = set()

        for edge in self.edges:
            x_set.add(edge[0])
            y_set.add(edge[1])

        return x_set, y_set
