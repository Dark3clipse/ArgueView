from ToastApi.Rule import Rule
from typing import List


class KnowledgeBaseRule(Rule):

    _r: str
    _args: List[str]
    _ruleArgList: List[str] = None

    def __init__(self, rule: str, args: List[str] = [], label: str = None):
        self._r = rule
        self._args = args
        self._lbl = label

    def _compile_arglist(self) -> str:
        str = ""
        for i in range(len(self._args)):
            str += self._args[i]
            if i+1<len(self._args):
                str += ", "
        return str

    def _compile_arglist_abstract(self) -> str:
        str = ""
        for i in range(len(self._args)):
            if self._ruleArgList is None:
                str += "X"
            else:
                str += self._ruleArgList[i]
            if i + 1 < len(self._args):
                str += ", "
        return str

    def compile(self, top_level: bool = True) -> str:
        return self._r+("("+self._compile_arglist()+")" if top_level else "("+self._compile_arglist_abstract()+")")

    def A(self, args: List[str]):
        self._ruleArgList = args
        return self

    def G(self) -> str:
        return self._r
