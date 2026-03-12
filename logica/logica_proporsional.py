from sympy import symbols, Or, And, Not, Implies
from sympy.logic.boolalg import truth_table
C, R, E = symbols('C R E')

B = Or(And(C, R), E)

for inputs, value in truth_table(B, [C, R, E]):
    print(dict(zip(['C','R','E'], inputs)), value)