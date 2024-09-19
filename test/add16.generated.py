from thdl.adders import Add4
from thdl.basic_components import HalfAdder, FullAdder
from thdl.val import Val, ValList
from thdl.chip import Chip, Chip_SO

class Add16(Chip):
    def __init__(self):
        self.add4_1 = Add4()
        self.add4_2 = Add4()
        self.add4_3 = Add4()
        self.add4_4 = Add4()
        self.carry1 = None
        self.carry3 = None
        self.carry2 = None
        self.a = None
        self.b = None
        self.carry_in = None
        super().__init__()

    def __call__(self, a: ValList, b: ValList, carry_in: Val):
        self.add4_1 = self.add4_1(a=self.a[12:15], b=self.b[12:15], carry_in=self.carry_in, sum=self.sum[0:3], carry_out=self.carry1)
        self.add4_2 = self.add4_2(a=self.a[8:11], b=self.b[8:11], carry_in=self.carry1, sum=self.sum[4:7], carry_out=self.carry2)
        self.add4_3 = self.add4_3(a=self.a[4:7], b=self.b[4:7], carry_in=self.carry2, sum=self.sum[8:11], carry_out=self.carry3)
        self.add4_4 = self.add4_4(a=self.a[0:3], b=self.b[0:3], carry_in=self.carry3, sum=self.sum[12:15], carry_out=self.carry_out)
