from thdl.chip import Chip
from thdl.gates import And, Or, Xor
from thdl.val import Val


class HalfAdder(Chip):
    def __init__(self):
        self.xor_gate = Xor()
        self.and_gate = And()

    def __call__(self, a: Val, b: Val) -> dict[str, Val]:
        return {
            'sum': self.xor_gate(a=a, b=b),
            'carry': self.and_gate(a=a, b=b)
        }


class FullAdder(Chip):
    def __init__(self):
        self.half_adder_1 = HalfAdder()
        self.half_adder_2 = HalfAdder()
        self.or_gate = Or()

    def __call__(self, a: Val, b: Val, c: Val) -> dict[str, Val]:
        half_adder_1 = self.half_adder_1(a=a, b=b)
        half_adder_2 = self.half_adder_2(a=half_adder_1['sum'], b=c)
        return {
            'sum': half_adder_2['sum'],
            'carry': self.or_gate(a=half_adder_1['carry'], b=half_adder_2['carry'])
        }
