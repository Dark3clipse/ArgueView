from ToastApi.KnowledgeBaseRule import KnowledgeBaseRule
from typing import List


class Premise(KnowledgeBaseRule):
    def __init__(self, rule: str, args: List[str]):
        super(Premise, self).__init__(rule, args)
