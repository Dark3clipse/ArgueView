from typing import List
from ToastApi.Axiom import Axiom
from ToastApi.Premise import Premise
from ToastApi.Assumption import Assumption
from ToastApi.KnowledgePreference import KnowledgePreference
from ToastApi.RegularRule import RegularRule
from ToastApi.Contrariness import Contrariness
from ToastApi.RulePreference import RulePreference
from ToastApi.Consequent import Consequent
from ToastApi.KnowledgeBaseRule import KnowledgeBaseRule
from ToastApi.Rule import Rule
import json
import requests


class ToastApi:

    LINK_WEAKEST = "weakest"
    _link: str = "weakest"

    SEMANTICS_GROUNDED = "grounded"
    _semantics: str = "grounded"

    _axioms: List[KnowledgeBaseRule]
    _premises: List[KnowledgeBaseRule]
    _assumptions: List[KnowledgeBaseRule]
    _preferences: List[KnowledgePreference]
    _rulePreferences: List[RulePreference]
    _rules: List[RegularRule]
    _contrarinesses: List[Contrariness]

    _endpoint = "http://toast.arg-tech.org/api"

    #def __init__(self):

    def setLink(self, link_type: str):
        self._link = link_type

    def setSemantics(self, semantics_type: str):
        self._semantics = semantics_type

    def setAxioms(self, axioms: List[KnowledgeBaseRule]) -> None:
        self._axioms = axioms

    def setPremises(self, premises: List[KnowledgeBaseRule]) -> None:
        self._premises = premises

    def setAssumptions(self, assumptions: List[KnowledgeBaseRule]) -> None:
        self._assumptions = assumptions

    def setPreferences(self, preferences: List[KnowledgePreference]) -> None:
        self._preferences = preferences

    def setRules(self, rules: List[RegularRule]) -> None:
        self._rules = rules

    def setRulePreferences(self, preferences: List[RulePreference]) -> None:
        self._rulePreferences = preferences

    def setContrarinesses(self, contrarinesses: List[Contrariness]) -> None:
        self._contrarinesses = contrarinesses

    def _compile_list(self, list: List[Rule]) -> List[str]:
        l = []
        for i in range(len(list)):
            l.append(list[i].compile())
        return l

    def compile(self, query: str) -> str:
        return json.dumps({
            "link": self._link,
            "semantics": self._semantics,
            "axioms": self._compile_list(self._axioms),
            "premises": self._compile_list(self._premises),
            "assumptions": self._compile_list(self._assumptions),
            "kbPrefs": self._compile_list(self._preferences),
            "rules": self._compile_list(self._rules),
            "rulePrefs": self._compile_list(self._rulePreferences),
            "contrariness": self._compile_list(self._contrarinesses),
            "query": query
        })

    def evaluate(self, query: str) -> str:
        payload = self.compile(query)
        print(json.dumps(payload.replace("\\", ""), indent=4, sort_keys=True))
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        r = requests.post(self._endpoint+"/evaluate", data=payload, headers=headers, verify=False)
        if r.status_code == 200:
            return r.text
        else:
            return ""
