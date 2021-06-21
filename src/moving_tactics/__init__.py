from field_analyser import FieldAnalyser


class IMovingTactics:
    def __init__(self, field_analyser: FieldAnalyser):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()
