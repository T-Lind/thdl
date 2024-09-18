from thdl.basic_components import FullAdder
from thdl.chip import Chip
from thdl.val import Val


class Add4(Chip):
    def __init__(self):
        super().__init__()
        self.full_adder_1 = FullAdder()
        self.full_adder_2 = FullAdder()
        self.full_adder_3 = FullAdder()
        self.full_adder_4 = FullAdder()

    def __call__(self, carry_in: Val, a: list[Val], b: list[Val]) -> dict[str, list[Val]]:
        print("a", a)
        print("b", b)

        fa1 = self.full_adder_1(a=a[3], b=b[3], c=carry_in)
        fa2 = self.full_adder_2(a=a[2], b=b[2], c=fa1['carry'])
        fa3 = self.full_adder_3(a=a[1], b=b[1], c=fa2['carry'])
        fa4 = self.full_adder_4(a=a[0], b=b[0], c=fa3['carry'])
        sum_result = [fa1['sum'], fa2['sum'], fa3['sum'], fa4['sum']]
        sum_result = list(reversed(sum_result))

        return {
            'sum': sum_result,
            'carry_out': fa4['carry']
        }
