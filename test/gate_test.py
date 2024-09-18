from thdl.adders import Add16
from thdl.val import Val, ValList


sixteen_adder = Add16()

a = ValList(0b1000001110111011)
b = ValList(0b1000000110011001)

print("a", a)
print("b", b)

result = sixteen_adder(a=a, b=b, carry_in=Val(0b0))
print(result)
