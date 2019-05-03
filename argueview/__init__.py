from typing import List
from typing import Tuple


class ArgueView:

    expmap: List[Tuple[int, int]]

    decision: int
    classes: List
    features: List
    support: List[Tuple[int, int]]
    attack: List[Tuple[int, int]]

    _grounds: List[Tuple[str, str]]
    _feature_specific: List[List[any]]

    def __init__(self, decision: int, classes: List[str], features: List, explanation_map: List[Tuple[int, int]]) -> None:
        self.decision = decision
        self.classes = classes
        self.features = features
        self.expmap = explanation_map

        # find support and attack based on decision and explanation map
        self.filterExplanationDirection()

        # print
        print(self.expmap)
        print(self.support)
        print(self.attack)

    def grounds(self, _grounds: List[Tuple[str, str]], feature_specific: List[List[any]]) -> object:
        self._grounds = _grounds
        self._feature_specific = feature_specific


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
        print("Decision: "+str(self.classes[self.decision]))
        for t in self.support:
            feature = t[0]
            strength = t[1]
            print(self.compileText(self._grounds[feature][self.decision], value=int(self.features[feature]), options=self._feature_specific[feature]))


