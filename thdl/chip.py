from abc import ABC, abstractmethod

from thdl.val import Val


class Chip_SO(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Val:
        pass


class Chip(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs) -> dict:
        pass
