from ToastApi.KnowledgeBaseRule import KnowledgeBaseRule
from typing import List


class Assumption(KnowledgeBaseRule):
    def __init__(self, rule: str, args: List[str]):
        super(Assumption, self).__init__(rule, args)
