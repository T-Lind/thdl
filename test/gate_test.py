from thdl.adders import Add4
from thdl.val import Val, from_list

four_adder = Add4()

a = from_list(1, 0, 1, 1)
b = from_list(1, 0, 0, 1)

result = four_adder(a=a, b=b, carry_in=Val(0))
print(result)
