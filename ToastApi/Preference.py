from ToastApi.Rule import Rule


class Preference(Rule):

    TYPE_KNOWLEDGE = 0
    TYPE_RULE = 1

    _type: int
    _better: Rule
    _lesser: Rule

    def __init__(self, preftype: int, better: Rule, lesser: Rule, label: str = None):
        self._type = preftype
        self._better = better
        self._lesser = lesser
        self._lbl = label

    def compile(self, top_level: bool = True) -> str:
        return self._lesser.compile(False)+"<"+self._better.compile(False)+("" if top_level else "")
