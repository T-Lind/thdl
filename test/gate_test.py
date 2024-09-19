from thdl.adders import Add16
from thdl.gates import Or
from thdl.val import Val, ValList


sixteen_adder = Add16()

a = ValList(0b1000001110111011)
b = ValList(0b1000000110011001)
result = sixteen_adder(a=a, b=b, carry_in=Val(0b0))

or_gate = Or()
or_result = or_gate(a=Val(0b0), b=Val(0b1))

