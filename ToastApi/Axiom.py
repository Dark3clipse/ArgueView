from ToastApi.KnowledgeBaseRule import KnowledgeBaseRule
from typing import List


class Axiom(KnowledgeBaseRule):
    def __init__(self, rule: str, args: List[str]):
        super(Axiom, self).__init__(rule, args)
