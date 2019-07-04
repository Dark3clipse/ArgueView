from ToastApi.Consequent import Consequent
from ToastApi.KnowledgeBaseRule import KnowledgeBaseRule
from ToastApi.Rule import Rule

from typing import List


class RegularRule(Rule):

    _antecedents: List[KnowledgeBaseRule]
    _consequent: Consequent
    _defeasible: bool

    def __init__(self, label: str, antecedents: List[KnowledgeBaseRule], consequent: Consequent, defeasible: bool = True):
        self._lbl = label
        self._antecedents = antecedents
        self._consequent = consequent
        self._defeasible = defeasible

    def compile(self, top_level: bool = True) -> str:
        if top_level:

            # label
            _str = "["+self._lbl+"] "

            # antecedents
            for i in range(len(self._antecedents)):
                _str += self._antecedents[i].compile(False)
                if i + 1 < len(self._antecedents):
                    _str += ", "

            # implication
            if self._defeasible:
                _str += " => "
            else:
                _str += " -> "

            # consequent
            _str += self._consequent.compile(False)

            return _str
        else:
            return "["+self._lbl+"]"
