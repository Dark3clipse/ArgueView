from ToastApi.Preference import Preference
from ToastApi.RegularRule import RegularRule


class RulePreference(Preference):
    def __init__(self, label: str, better: RegularRule, lesser: RegularRule):
        super(RulePreference, self).__init__(Preference.TYPE_RULE, better, lesser, label)