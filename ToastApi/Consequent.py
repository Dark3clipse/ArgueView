from ToastApi.KnowledgeBaseRule import KnowledgeBaseRule
from typing import List


class Consequent(KnowledgeBaseRule):
    def __init__(self, rule: str, args: List[str]):
        super(Consequent, self).__init__(rule, args)
