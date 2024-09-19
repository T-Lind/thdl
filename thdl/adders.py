from thdl.basic_components import FullAdder
from thdl.chip import Chip
from thdl.val import Val, ValList


class Add4(Chip):
    def __init__(self):
        self.full_adder_1 = FullAdder()
        self.full_adder_2 = FullAdder()
        self.full_adder_3 = FullAdder()
        self.full_adder_4 = FullAdder()
        super().__init__()

    def __call__(self, carry_in: Val, a: ValList, b: ValList) -> dict[str, ValList | Val]:
        fa1 = self.full_adder_1(a=a[0], b=b[0], c=carry_in)
        fa2 = self.full_adder_2(a=a[1], b=b[1], c=fa1['carry'])
        fa3 = self.full_adder_3(a=a[2], b=b[2], c=fa2['carry'])
        fa4 = self.full_adder_4(a=a[3], b=b[3], c=fa3['carry'])
        sum_result = [fa1['sum'], fa2['sum'], fa3['sum'], fa4['sum']]
        sum_result = list(reversed(sum_result))
        sum_result = ValList(list=sum_result)

        return {
            'sum': sum_result,
            'carry_out': fa4['carry']
        }


# chain together add4's for Add16

class Add16(Chip):
    def __init__(self):
        self.add4_1 = Add4()
        self.add4_2 = Add4()
        self.add4_3 = Add4()
        self.add4_4 = Add4()
        super().__init__()

    def __call__(self, carry_in: Val, a: ValList, b: ValList) -> dict[str, ValList]:
        add4_1 = self.add4_1(carry_in=carry_in, a=a[12:], b=b[12:])
        add4_2 = self.add4_2(carry_in=add4_1['carry_out'], a=a[8:12], b=b[8:12])
        add4_3 = self.add4_3(carry_in=add4_2['carry_out'], a=a[4:8], b=b[4:8])
        add4_4 = self.add4_4(carry_in=add4_3['carry_out'], a=a[:4], b=b[:4])

        sum_result = add4_4['sum'] + add4_3['sum'] + add4_2['sum'] + add4_1['sum']
        carry_out = add4_4['carry_out']

        return {
            'sum': sum_result,
            'carry_out': carry_out
        }
