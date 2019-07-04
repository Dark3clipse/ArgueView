from ToastApi.Preference import Preference
from ToastApi.KnowledgeBaseRule import KnowledgeBaseRule


class KnowledgePreference(Preference):
    def __init__(self, label: str, better: KnowledgeBaseRule, lesser: KnowledgeBaseRule):
        super(KnowledgePreference, self).__init__(Preference.TYPE_KNOWLEDGE, better, lesser, label)