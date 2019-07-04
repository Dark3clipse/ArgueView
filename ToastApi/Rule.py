from abc import ABC, abstractmethod


class Rule(ABC):

    _lbl: str

    @abstractmethod
    def compile(self, top_level: bool = True) -> str:
        pass
