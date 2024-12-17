from main import *
b = main_dict['demand_quantities'][0]

while True:
    main_dict['demand_quantities'][0] += 1
    a = main_lp()
    if a == -1:
        break

print('We are still in feasible region if we increase demand quantity 0 by', main_dict['demand_quantities'][0] -b -1)
# -1 is here because the loop fails at the first infeasible solution