from typing import List
from typing import Tuple
import http.server
import socketserver
import webbrowser
import json
from Dataset import *


class ArgueView:

    expmap: List[Tuple[int, int]]

    data: Dataset
    decision: int
    classes: List
    features: List
    support: List[Tuple[int, int]]
    attack: List[Tuple[int, int]]

    _grounds: List[Tuple[str, str]]
    _feature_specific: List[List[any]]
    _conclusions: List[str]
    _probabilities: any
    _qualifier: float
    _backing: any
    _input: any

    def __init__(self, dataset: Dataset, decision: int, classes: List[str], features: List, explanation_map: List[Tuple[int, int]]) -> None:
        self.data = dataset
        self.decision = decision
        self.classes = classes
        self.features = features
        self.expmap = explanation_map

        # find support and attack based on decision and explanation map
        self.filterExplanationDirection()

    def grounds(self, _grounds: List[Tuple[str, str]], feature_specific: List[List[any]]) -> object:
        self._grounds = _grounds
        self._feature_specific = feature_specific

    def conclusions(self, _conclusions: List[str]) -> None:
        self._conclusions = _conclusions

    def backing(self, _backing: any) -> None:
        self._backing = _backing

    def classProbabilities(self, proba) -> None:
        self._probabilities = proba

    def input(self, input: any) -> None:
        self._input = input

    def filterExplanationDirection(self) -> None:
        positive = []
        negative = []

        for t in self.expmap[1]:
            strength = t[1]
            if strength > 0:
                positive.append(t)
            else:
                negative.append(t)

        if self.decision == 0:
            self.support = negative
            self.attack = positive
        else:
            self.support = positive
            self.attack = negative

    def compileText(self, _str: str, value: int, options: List[any]) -> str:
        if (value >= len(options)):
            return _str
        return _str.replace("<>", options[value])

    def printExplanationGrounds(self) -> None:
        print("Decision: "+str(self._conclusions))
        for t in self.support:
            feature = t[0]
            strength = t[1]
            print(self.compileText(self._grounds[feature][self.decision], value=int(self.features[feature]), options=self._feature_specific[feature]))

    def computeQualifier(self) -> str:
        proba_decision = self._probabilities[self.decision]
        proba_uncertain = 1 / len(self._probabilities)
        full_range = (1 - proba_uncertain)
        pos = proba_decision - proba_uncertain
        self._qualifier = pos / full_range

    def compileQualifier(self) -> str:
        return "This decision is {:.0f}% more certain than the other possible outcomes.".format(100*self._qualifier)

    def compileNumber(self, val: int) -> str:
        if val < 10:
            switcher = {
                0: "zero",
                1: "one",
                2: "two",
                3: "three",
                4: "four",
                5: "five",
                6: "six",
                7: "seven",
                8: "eight",
                9: "nine"
            }
            return switcher.get(val)
        return str(val)

    def compileDurationFormat(self, format: str, value: str) -> str:
        switcher = {
            "since": "since "+value,
            "for": "for "+value
        }
        return switcher.get(format)

    def compileBacking(self) -> str:
        st = "This decision is supported by "+self._backing.get("organization").get("name")+\
              ", who have employed the automatic decision-making model "+self._backing.get("model").get("name")+\
              ". This model is correct for {:.0f}% or the cases and is based on ".format(100*self.data.accuracy())
        if len(self._backing.get("data").get("sources"))>1:
            st+=self.compileNumber(len(self._backing.get("data").get("sources")))+" data sources. "
        else:
            st+="the <a target=\"_blank\" href=\""+self._backing.get("data").get("sources")[0].get("href")+"\">"+self._backing.get("data").get("sources")[0].get("name")+" dataset<a>. "
            if self._backing.get("data").get("sources")[0].get("type")=="static":
                st+="This dataset is collected in "+str(self._backing.get("data").get("sources")[0].get("year"))+" by "+self._backing.get("data").get("sources")[0].get("author").get("name")+" of "+self._backing.get("data").get("sources")[0].get("author").get("organization")+". "
        st+="The "+self._backing.get("model").get("name")+" model is developed by "+self._backing.get("developer").get("name")+", who "+("have" if self._backing.get("developer").get("plural") else "has")+\
             " been active in decision-making model development "+self.compileDurationFormat(self._backing.get("developer").get("operation_duration").get("format"), self._backing.get("developer").get("operation_duration").get("value"))+". "
        return st

    def importance(self) -> any:
        rt = []
        for i in range(len(self.expmap[1])):
            rt.append({"feature": int(self.expmap[1][i][0]), "contribution": float(self.expmap[1][i][1])})
        return rt

    def show(self) -> None:

        support = []
        for t in self.support:
            support.append({"feature": int(t[0]), "strength": t[1], "text": self.compileText(self._grounds[t[0]][self.decision], value=int(self.features[t[0]]), options=self._feature_specific[t[0]])})

        self.computeQualifier()
        qualifier = {
            "value": self._qualifier,
            "text": self.compileQualifier()
        }

        json_data = {
            "decision": str(self._conclusions[self.decision]),
            "support": support,
            "qualifier": qualifier,
            "backing": {
                "text": self.compileBacking(),
                "data": self._backing
            },
            "input": self._input
        }
        print(json_data)

        # write to json
        filename_out = 'assets/explanation.json'
        json_out = open(filename_out, 'w')
        json_out.write(json.dumps(json_data, indent=1, sort_keys=True))
        json_out.close()

        # start server
        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            webbrowser.open("http://localhost:8000/assets/explanation.html")
            httpd.serve_forever()