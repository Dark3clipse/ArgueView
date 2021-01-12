from typing import List, Union
from argueview.typings import Source, Explanation, Case, Data, ExplanationPartial, FeatureExplanation, Grounds, \
    GroundsVarByClass, FeatureImportance, Feature, LatentContinuousTarget


class ArgueView:
    """Argumentative explanation presentation tool for machine-learning and decision-support systems.

    ArgueView provides functionality to organize contextual information about your data sources, the decision-classes,
    feature-importance based explanations, and a decision backing. With provided information ArgueView can generate a
    json-styled data explanation object that can be exported and used in visualization tools.
    """

    _backing: str
    _sources: List[Source]
    _classes: List[str]
    _lct: LatentContinuousTarget
    _grounds: Grounds
    _grounds_vars: GroundsVarByClass

    _case: Case
    _fimportance: List[FeatureImportance]
    _unexplained: float
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
        if hasattr(self, '_lct') and len(self._lct.mapping) != len(classes):
            raise Exception(
                'The number of classes should match the length of the defined latent continuous target mapping.')
        self._classes = classes

    def latent_continuous_target(self, label: str, anti_label: str, mapping: List[float]) -> None:
        """Define a latent continuous target present within your decision-classes.

        To illustrate the usage of the latent continuous target assume a decision task in the loan application domain
        where predictions determine whether someone is eligible for a loan. The decision-classes are: 'applicable for loan'
        and 'not applicable for loan'. In this scenario the latent continuous target is 'applicability' and it's anti-label
        is 'inapplicability'. The mapping is [1, -1] which indicates the value of the latent target for each decision-class.

        :param label: Label for the latent continuous target.
        :param anti_label: Anti-label for the latent continuous target.
        :param mapping: List of values representing the value of the latent target for each decision-class.
        :return:
        """
        if hasattr(self, '_classes') and len(self._classes) != len(mapping):
            raise Exception('Length of mapping should match the number of classes.')
        self._lct = LatentContinuousTarget({
            "label": label,
            "anti_label": anti_label
        })
        self._lct.mapping = mapping

    def backing(self, backing: str) -> None:
        """Defines textual backing to support your decisions.

        A strong backing should describe the data quality and the quality of the provider.

        :param  backing: A textual backing to support your decisions.
        :return:
        """

        self._backing = backing

    def grounds(self, grounds: Grounds, grounds_var_by_class: GroundsVarByClass) -> None:
        """Define grounds for the rationale of how each feature affects the decision-class.

        The grounds describe how features affect the decision in each possible decision-class. The grounds can contain
        tokens that should be replaced based on the feature value. The token used for this is `<>`.

        :param  grounds: Contains for each feature the rationale for each decision class. The format is List[List[str]] where the outer list represents each feature and the inner list each decision-class.
        :param  grounds_var_by_class:
        :return:
        """

        self._grounds = grounds
        self._grounds_vars = grounds_var_by_class

    def add_data_source(self, source: Source) -> None:
        """Add a data source to ArgueView. The data source describes the data origin and contents. It should follow the format defined in `Source`.

        :param  source: The data source description.
        :return:
        """

        self._sources.append(source)
        if not isinstance(source.features[0], Feature):
            for i in range(0, len(source.features)):
                self._sources[len(self._sources) - 1].features[i] = Feature(
                    self._sources[len(self._sources) - 1].features[i])

    def _ground_index(self, support: bool) -> int:
        """Determines the index of the ground to be shown when a feature supports or attacks the decision-class.

        :param  support: Whether a feature supports the decision class.
        :return: Ground index.
        """

        decision = self._case.decision_class()
        if support:
            return decision
        else:
            classes = len(self._classes)
            for x in range(classes-1, -1, -1):
                if x != decision:
                    return x
            return 0

    def _compile(self, source: int, feature: int, support: bool) -> str:
        """Compiles a rationale for a decision from a specific feature.

        :param  source: Data source index.
        :param  feature: Feature index.
        :param  support: Whether the feature supports the decision class.
        :return: A compiled rationale for the contribution of `feature` to the decision-class. Based on the grounds provided in ArgueView.grounds()
        """

        ground_index = self._ground_index(support)
        if not hasattr(self, '_grounds') or \
                not self._grounds or \
                feature >= len(self._grounds) or \
                source >= len(self._sources) or \
                not hasattr(self, '_case') or \
                not self._case or \
                source >= len(self._case.sources) or \
                feature >= len(self._case.sources[source].features) or \
                not hasattr(self._case.sources[source].features[feature], 'value') or \
                not hasattr(self, '_grounds_vars') or \
                feature >= len(self._grounds_vars) or \
                ground_index >= len(self._grounds[feature]):
            return ""

        ground = self._grounds[feature][ground_index]

        feature_value = int(self._case.sources[source].features[feature].value)
        options = self._grounds_vars[feature]
        if feature_value >= len(options):
            return ground
        return ground.replace("<>", options[feature_value])

    def _generate_explanation_partial(self) -> None:
        """Splits the feature contributions into support, attack, and base.

        :return:
        """

        positive = []
        negative = []
        for i in range(0, len(self._sources)):
            for t in self._fimportance[i]:
                valence = negative
                if t[1] > 0:
                    valence = positive
                contribution = float(t[1])
                valence.append(FeatureExplanation({
                    "source": i,
                    "feature": int(t[0]),
                    "contribution": contribution,
                    "value": self._compile(i, t[0], contribution >= 0)
                }))
        self._expPartial = ExplanationPartial({
            "support": positive,
            "attack": negative,
            "base": float(self._unexplained)
        })

    def generate(self, case: Case, feature_importance: Union[FeatureImportance, List[FeatureImportance]],
                 unexplained: float = 0) -> Explanation:
        """Generate an explanation for a case based on the given context.

        Generates an explanation for a specific case. This method uses the information provided by other methods and
        assembles this information and the current case into an explanation object. This object can be used to
        visualize the explanation or to export it for usage in other tools.

        :param case: Case object containing the class probabilities and feature values.
        :param feature_importance: Feature importance for the case as computed by an explainer. A list of FeatureImportance
        objects is required for multi-source scenarios.
        :param unexplained: Unexplained contribution for the decision-class.
        :return:
        """

        pre = 'cannot generate explanation: '
        if not hasattr(self, '_classes') or not self._classes:
            raise Exception(pre + 'no classes defined. Use ArgueView.classes to set your classes.')
        if not hasattr(self, '_grounds') or not self._grounds:
            print('Warning: Generating explanation without grounds.')
        if not hasattr(self, '_backing') or not self._backing:
            print('Warning: Generating explanation without a backing.')
        if not hasattr(self, '_sources') or not self._sources or len(self._sources) <= 0:
            raise Exception(pre + 'no data sources defined. Use ArgueView.add_data_source to add a data source.')

        if not isinstance(feature_importance[0], list):
            self._fimportance = [feature_importance]  # single list -> single source case
        else:
            self._fimportance = feature_importance  # input properly formatted
        self._unexplained = unexplained

        self._case = case
        self._generate_explanation_partial()
        _gen = Explanation()

        if hasattr(self, '_backing') and self._backing:
            _gen.backing = self._backing

        _gen.data = Data()
        _gen.data.classes = self._classes
        _gen.data.sources = self._sources
        _gen.data.latent_continuous_target = self._lct
        _gen.case = self._case
        _gen.explanation = self._expPartial
        return _gen
