from pccip.example.ex import lenghtOfEventLog
import os


class TestEx:
    def test_len(self):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        assert 51 == lenghtOfEventLog(os.path.join(
            currentDir, "roadtraffic50traces.xes"))
