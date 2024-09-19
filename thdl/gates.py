from thdl.chip import Chip_SO
from thdl.val import Val


# Basic Gates

class Not(Chip_SO):
    def __call__(self, a: Val):
        return Val(not a.value)


class And(Chip_SO):
    def __call__(self, a: Val, b: Val):
        return Val(a() and b())


class Or(Chip_SO):
    def __call__(self, a: Val, b: Val):
        return Val(a() or b())


# Composite Gates

class Nand(Chip_SO):
    def __init__(self):
        self.not_gate = Not()
        self.and_gate = And()

    def __call__(self, a: Val, b: Val):
        andAB = self.and_gate(a=a, b=b)
        return self.not_gate(a=andAB)


class Nor(Chip_SO):
    def __init__(self):
        self.not_gate = Not()
        self.or_gate = Or()

    def __call__(self, a: Val, b: Val):
        orAB = self.or_gate(a=a, b=b)
        return self.not_gate(a=orAB)


class Xor(Chip_SO):
    def __init__(self):
        self.and_gate = And()
        self.nor_1_gate = Nor()
        self.nor_2_gate = Nor()

    def __call__(self, a: Val, b: Val):
        andAB = self.and_gate(a=a, b=b)
        nor2AB = self.nor_2_gate(a=a, b=b)
        nor1AB = self.nor_1_gate(a=andAB, b=nor2AB)
        return nor1AB


class Xnor(Chip_SO):
    def __init__(self):
        self.xor_gate = Xor()
        self.not_gate = Not()

    def __call__(self, a: Val, b: Val):
        xorAB = self.xor_gate(a=a, b=b)
        return self.not_gate(a=xorAB)
