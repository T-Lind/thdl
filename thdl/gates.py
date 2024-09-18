from thdl.chip import Chip_SO
from thdl.val import Val


# Basic Gates

class NotGate(Chip_SO):
    def __call__(self, a: Val):
        return Val(not a.value)


class AndGate(Chip_SO):
    def __call__(self, a: Val, b: Val):
        return Val(a() and b())


class OrGate(Chip_SO):
    def __call__(self, a: Val, b: Val):
        return Val(a() or b())


# Composite Gates

class NandGate(Chip_SO):
    def __init__(self):
        self.not_gate = NotGate()
        self.and_gate = AndGate()

    def __call__(self, a: Val, b: Val):
        andAB = self.and_gate(a=a, b=b)
        return self.not_gate(a=andAB)


class NorGate(Chip_SO):
    def __init__(self):
        self.not_gate = NotGate()
        self.or_gate = OrGate()

    def __call__(self, a: Val, b: Val):
        orAB = self.or_gate(a=a, b=b)
        return self.not_gate(a=orAB)


class XorGate(Chip_SO):
    def __init__(self):
        self.and_gate = AndGate()
        self.nor_1_gate = NorGate()
        self.nor_2_gate = NorGate()

    def __call__(self, a: Val, b: Val):
        andAB = self.and_gate(a=a, b=b)
        nor2AB = self.nor_2_gate(a=a, b=b)
        nor1AB = self.nor_1_gate(a=andAB, b=nor2AB)
        return nor1AB


class XnorGate(Chip_SO):
    def __init__(self):
        self.xor_gate = XorGate()
        self.not_gate = NotGate()

    def __call__(self, a: Val, b: Val):
        xorAB = self.xor_gate(a=a, b=b)
        return self.not_gate(a=xorAB)
