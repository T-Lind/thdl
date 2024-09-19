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
        self._initialized = True

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    def __setattr__(self, name, value):
        if hasattr(self, '_initialized') and self._initialized:
            raise RuntimeError("Sub-chips or gates must be declared in __init__")
        super().__setattr__(name, value)
