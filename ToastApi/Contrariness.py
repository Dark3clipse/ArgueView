from ToastApi.KnowledgeBaseRule import KnowledgeBaseRule
from ToastApi.Rule import Rule


class Contrariness(Rule):

    _first: KnowledgeBaseRule
    _second: KnowledgeBaseRule

    def __init__(self, label: str, first: KnowledgeBaseRule, second: KnowledgeBaseRule):
        self._lbl = label
        self._first = first
        self._second = second

    def compile(self, top_level: bool = True) -> str:
        return self._first.compile(False)+"-"+self._second.compile(False)+("" if top_level else "")

