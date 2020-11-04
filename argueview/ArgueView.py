from typing import List, Union
from argueview.typings import Source, Explanation, Case, Data, ExplanationPartial, FeatureExplanation, Grounds, \
    GroundsVarByClass, FeatureImportance, Feature


class ArgueView:
    """Argumentative explanation presentation tool for machine-learning and decision-support systems.

    ArgueView provides functionality to organize contextual information about your data sources, the decision-classes,
    feature-importance based explanations, and a decision backing. With provided information ArgueView can generate a
    json-styled data explanation object that can be exported and used in visualization tools.
    """

    _backing: str
    _sources: List[Source]
    _classes: List[str]
    _grounds: Grounds
    _grounds_vars: GroundsVarByClass

    _case: Case
    _fimportance: FeatureImportance
    _gen: Explanation

    _expPartial: ExplanationPartial

    def __init__(self) -> None:
        self._sources = []

    def classes(self, classes: List[str]) -> None:
        """Defines textual representations for the decision-classes.

        For example, your decision task is a binary classification of pears and oranges, encoded as 0 or 1.
        You should then call this method with human-interpretable text representations for each class.
        An example would be classes = ['pears', 'orange']

        :param  classes: Array of textual representations for your decision-classes.
        :return:
        """

        self._classes = classes

    def backing(self, backing: str) -> None:
        """Defines textual backing to support your decisions.

        A strong backing should describe the data quality and the quality of the provider.

        :param  backing: A textual backing to support your decisions.
        :return:
        """

        self._backing = backing

    def grounds(self, grounds: Grounds, grounds_var_by_class: GroundsVarByClass) -> None:
        self._grounds = grounds
        self._grounds_vars = grounds_var_by_class

    def add_data_source(self, source: Source) -> None:
        self._sources.append(source)
        if not isinstance(source.features[0], Feature):
            for i in range(0, len(source.features)):
                self._sources[len(self._sources)-1].features[i] = Feature(self._sources[len(self._sources)-1].features[i])

    def _compile(self, decision: int, source: int, feature: int) -> str:
        """Compiles a rationale for a decision from a specific feature.

        :param  decision: The decision-class.
        :param  source: Data source.
        :param  feature: Feature number.
        :return: A compiled rationale for the contribution of `feature` to the decision-class. Based on the grounds provided in ArgueView.grounds()
        """

        ground = self._grounds[feature][decision]
        feature_value = int(self._case.sources[source].features[feature].value)
        options = self._grounds_vars[feature]
        if (feature_value >= len(options)):
            return ground
        return ground.replace("<>", options[feature_value])

    def _generateExplanationPartial(self) -> None:
        positive = []
        negative = []
        decision = self._case.decision_class()
        for i in range(0, len(self._sources)):
            for t in self._fimportance[i]:
                valence = negative
                if t[1] > 0:
                    valence = positive
                valence.append(FeatureExplanation({
                    "source": i,
                    "feature": t[0],
                    "contribution": t[1],
                    "value": self._compile(decision, i, t[0])
                }))
        self._expPartial = ExplanationPartial({
            "support": positive,
            "attack": negative
        })

    def generate(self, case: Case, feature_importance: Union[FeatureImportance, List[FeatureImportance]]) -> Explanation:
        pre = 'cannot generate explanation: '
        if not self._classes:
            raise Exception(pre+'no classes defined. Use ArgueView.classes to set your classes.')
        if not self._grounds:
            raise Exception(pre+'no grounds defined. Use ArgueView.grounds to set your grounds.')
        if not self._backing:
            print('Warning: Generating explanation without a backing.')
        if not self._sources or len(self._sources) <= 0:
            raise Exception(pre+'no data sources defined. Use ArgueView.add_data_source to add a data source.')

        self._case = case
        self._fimportance = feature_importance if isinstance(feature_importance[0], list) else [feature_importance]
        self._generateExplanationPartial()
        _gen = Explanation()

        if self._backing:
            _gen.backing = self._backing

        _gen.data = Data()
        _gen.data.classes = self._classes
        _gen.data.sources = self._sources
        _gen.case = self._case
        _gen.explanation = self._expPartial
        return _gen
