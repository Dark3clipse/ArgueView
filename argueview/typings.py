import enum
import textwrap
from random import random
from typing import List, Union, NewType, Tuple
import jsonpickle


class DummyUpdater(object):
    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)


class Author(DummyUpdater):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable, **kwargs)

    name: str
    organization: str


class Feature(DummyUpdater):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable, **kwargs)

    data_type: str
    description: str
    index: int
    is_ignore: bool
    is_row_identifier: bool
    is_target: bool
    name: str
    nominal_value: List[str]
    number_of_missing_values: int

    def __setitem__(self, key: str, value: any) -> None:
        self[key] = value


class Source(DummyUpdater):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable, **kwargs)

    name: str
    author: Author
    description: str
    href: str
    observations: int
    type: str
    year: int
    features: List[Feature]


class OpenMLFeatureData(DummyUpdater):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable, **kwargs)

    feature: List[Feature]


class CaseFeature(DummyUpdater):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable, **kwargs)

    value: Union[float, str]


class CaseSource(DummyUpdater):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable, **kwargs)

    features: List[CaseFeature]


class Case(DummyUpdater):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable, **kwargs)

    id: int
    class_proba: List[float]
    sources: List[CaseSource]

    def decision_class(self) -> int:
        return self.class_proba.index(max(self.class_proba))

    def qualifier(self) -> float:
        proba_decision = self.class_proba[self.decision_class()]
        proba_uncertain = 1 / len(self.class_proba)
        full_range = (1 - proba_uncertain)
        pos = proba_decision - proba_uncertain
        return pos / full_range


class LatentContinuousTarget(DummyUpdater):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable, **kwargs)

    label: str
    anti_label: str
    mapping: List[float]


class Data(DummyUpdater):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable, **kwargs)

    classes: List[str]
    latent_continuous_target: LatentContinuousTarget
    sources: List[Source]


class FeatureExplanation(DummyUpdater):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable, **kwargs)

    source: int
    feature: int
    value: str
    contribution: float


class ExplanationPartial(DummyUpdater):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable, **kwargs)

    base: float
    support: List[FeatureExplanation]
    attack: List[FeatureExplanation]

    def find(self, source: int, feature: int) -> Union[FeatureExplanation, None]:
        l: List[FeatureExplanation] = [*self.support, *self.attack]
        for i in range(0, len(l)):
            if l[i].source == source and l[i].feature == feature:
                return l[i]
        return None


class Color:
    BOLD = '\033[1m'
    END = '\033[0m'


class Explanation(DummyUpdater):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable, **kwargs)

    backing: str
    case: Case
    data: Data
    explanation: ExplanationPartial

    def serialize(self) -> str:
        return jsonpickle.encode(self, unpicklable=False)

    def save(self, fname: str, pretty: bool = True) -> None:
        json_out = open(fname, 'w')
        if pretty:
            jsonpickle.set_encoder_options('json', indent=4)
        else:
            jsonpickle.set_encoder_options('json')
        json_out.write(self.serialize())
        json_out.close()

    def feature_value(self, source: int, feature: int) -> Union[str, int, float]:
        if source >= len(self.case.sources) or feature >= len(self.case.sources[source].features):
            return 0
        val = self.case.sources[source].features[feature].value
        fdata = self.data.sources[source].features[feature]
        if fdata.data_type == 'nominal':
            return fdata.nominal_value[int(val)]
        else:
            return val

    def _print_multiline(self, inpstr: str, str_pre: str, str_post: str, str_max_length: int, max_length: int,
                         cl: int) -> None:
        if len(inpstr) - cl <= max_length:
            print(str_pre + inpstr + ' ' * (str_max_length - len(inpstr) + cl) + str_post)
        else:
            inpstr_lines = textwrap.wrap(inpstr, max_length)
            for i in range(0, len(inpstr_lines)):
                print(str_pre + inpstr_lines[i] + ' ' * (
                        str_max_length - len(inpstr_lines[i]) + (cl if i == 0 else 0)) + str_post)

    def print(self, plain=False) -> None:

        # compute variables
        dclass = self.data.classes[self.case.decision_class()]
        support_max = 0
        support_i = 0
        for i in range(0, len(self.explanation.support)):
            if self.explanation.support[i].contribution > support_max:
                support_max = self.explanation.support[i].contribution
                support_i = i
        lrat = self.explanation.support[support_i].value

        if plain:
            print('Explanation')
            print('class: ' + dclass)
            if lrat and len(lrat)>0:
                print('leading rationale:' + lrat)
            print(
                'qualifier: ' + "The class '" + dclass + "' is {:.0f}% more certain than the other possible classes.".format(
                    100 * self.case.qualifier()))
            if hasattr(self, 'backing') and len(self.backing) > 0:
                print('backing: ' + self.backing)
            print()
            for i in range(0, len(self.case.sources)):
                print('Source: ' + self.data.sources[i].name)
                names = []
                vals = []
                cont = []
                contval = []
                for j in range(0, len(self.data.sources[i].features)):
                    ef = self.explanation.find(i, j)
                    names.append(self.data.sources[i].features[j].name)
                    vals.append(str(self.feature_value(i, j)))
                    cont.append((str(ef.contribution) if ef is not None else "None"))
                    contval.append(ef.contribution if ef is not None else -999999)
                names_max_length = max(map(lambda x: len(x), names))
                vals_max_length = max(map(lambda x: len(x), vals))
                for j in range(0, len(names)):
                    print(names[j] + ' ' * (names_max_length - len(names[j])) + ' = ' + vals[j] + ' ' * (
                            vals_max_length - len(vals[j])) + ' , contribution = ' + cont[j])
                print()
            print('Unexplained contribution: ' + str(self.explanation.base))

        else:
            # compute strings
            str_header = '-- Explanation '
            str_pre = '|  '
            str_post = '  |'
            str_class = Color.BOLD + 'class: ' + Color.END + dclass
            if lrat and len(lrat) > 0:
                str_lrat = Color.BOLD + 'leading rationale: ' + Color.END + lrat
            else:
                str_lrat = ""
            str_qualifier = Color.BOLD + "qualifier: " + Color.END + "The class '" + dclass + "' is {:.0f}% more certain than the other possible classes.".format(
                100 * self.case.qualifier())
            if hasattr(self, 'backing') and len(self.backing) > 0:
                str_backing = Color.BOLD + 'backing: ' + Color.END + self.backing
            else:
                str_backing = ""

            # print explanation
            max_length = 80
            cl = len(Color.BOLD) + len(Color.END)
            str_max_length = min(max_length, max(len(str_class), len(str_lrat), len(str_qualifier), len(str_backing)))
            print('\n' + str_header + '-' * (str_max_length - len(str_header) + len(str_pre) + len(str_post)))
            self._print_multiline(str_class, str_pre, str_post, str_max_length, max_length, cl)
            if lrat and len(lrat) > 0:
                self._print_multiline(str_lrat, str_pre, str_post, str_max_length, max_length, cl)
            self._print_multiline(str_qualifier, str_pre, str_post, str_max_length, max_length, cl)
            if hasattr(self, 'backing') and len(self.backing) > 0:
                self._print_multiline(str_backing, str_pre, str_post, str_max_length, max_length, cl)
            print('-' * (str_max_length + len(str_pre) + len(str_post)) + '\n')

            for i in range(0, len(self.case.sources)):

                # compute strings for source
                str_header = '-- ' + self.data.sources[i].name + ' '
                names = []
                vals = []
                cont = []
                contval = []
                for j in range(0, len(self.data.sources[i].features)):
                    ef = self.explanation.find(i, j)
                    names.append(self.data.sources[i].features[j].name)
                    vals.append(str(self.feature_value(i, j)))
                    cont.append((str(ef.contribution) if ef is not None else "None"))
                    contval.append(ef.contribution if ef is not None else -999999)
                names_max_length = max(map(lambda x: len(x), names))
                vals_max_length = max(map(lambda x: len(x), vals))
                content = []
                for j in range(0, len(names)):
                    content.append(names[j] + ' ' * (names_max_length - len(names[j])) + ' = ' + vals[j] + ' ' * (
                            vals_max_length - len(vals[j])) + ' , contribution = ' + cont[j])
                str_max_length = max(map(lambda x: len(x), content))

                # sort based on contribution
                content = list(zip(*sorted(zip(contval, content), reverse=True)))[1]

                # print source
                print(str_header + '-' * (str_max_length - len(str_header) + len(str_pre) + len(str_post)))
                for j in range(0, len(content)):
                    print(str_pre + content[j] + ' ' * (str_max_length - len(content[j])) + str_post)
                print('-' * (str_max_length + len(str_pre) + len(str_post)))
            print('Unexplained contribution: ' + str(self.explanation.base))


class Framing(enum.Enum):
    positive = 'positive'
    negative = 'negative'
    original = 'original'


class LatentContinuousTargetDisplay(enum.Enum):
    positive = 'label'
    negative = 'anti-label'
    none = 'none'


class FeatureListVisualizationType(enum.Enum):
    badge = 'badge'
    bar = 'bar'


Ground = NewType('Ground', List[str])
Grounds = NewType('Grounds', List[Ground])
GroundVarByClass = NewType('GroundVarByClass', List[str])
GroundsVarByClass = NewType('GroundsVarByClass', List[GroundVarByClass])
FeatureImportance = NewType('FeatureImportance', List[Tuple[int, float]])
