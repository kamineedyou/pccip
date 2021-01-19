import pytest
from pccip.bin.passages.passage import Passage


class Test_Passages:
    @pytest.fixture
    def validPassage(self):
        # from figure 2 in paper
        causal_example = {('d', 'd'), ('d', 'e'), ('b', 'e'),
                          ('b', 'd'), ('b', 'f'), ('c', 'f')}

        return Passage(causal_example)

    def test_ValidPassageInit(self, validPassage):

        assert isinstance(validPassage, Passage)
        assert ('d', 'e') in validPassage.edges
        assert len(validPassage.edges) == 6

        passage_2 = Passage()
        assert isinstance(passage_2, Passage)
        assert validPassage != passage_2

    def test_InvalidPassageInit(self):
        with pytest.raises(TypeError):
            Passage(('a', 'b'))

    def test_ValidPassageGetX(self, validPassage):
        test_object = validPassage.getX()
        assert isinstance(test_object, set)
        assert len(test_object) == 3
        assert 'd' in test_object and 'b' in test_object and 'c' in test_object

    def test_ValidPassageGetY(self, validPassage):
        test_object = validPassage.getY()
        assert isinstance(test_object, set)
        assert len(test_object) == 3
        assert 'd' in test_object and 'e' in test_object and 'f' in test_object

    def test_ValidPassageGetXY(self, validPassage):
        test_X, test_Y = validPassage.getXY()
        assert isinstance(test_X, set)
        assert isinstance(test_Y, set)
        assert len(test_X) == 3
        assert len(test_Y) == 3
        assert 'd' in test_X and 'b' in test_X and 'c' in test_X
        assert 'd' in test_Y and 'e' in test_Y and 'f' in test_Y

    def test_ValidPassageAddEdge(self, validPassage):
        test_add = ('a', 'b')
        test_add_set = {('a', 'b')}
        test_add_wrong_edge0 = (2, 'b')
        test_add_wrong_edge1 = ('a', 2)

        assert len(validPassage.edges) == 6
        validPassage.addEdge(test_add)
        assert len(validPassage.edges) == 7
        assert test_add in validPassage.edges
        validPassage.addEdge(test_add)
        assert len(validPassage.edges) == 7

        with pytest.raises(TypeError):
            validPassage.addEdge(test_add_set)
            validPassage.addEdge(test_add_wrong_edge0)
            validPassage.addEdge(test_add_wrong_edge1)
