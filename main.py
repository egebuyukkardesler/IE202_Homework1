import pulp

main_dict = {'c_S_T1': [[20, 22], [22, 20], [17, 28], [13, 17]],
             'c_T1_T2' : [[55, 57, 31, 33, 35], [37, 60, 36, 59, 46]],
             'c_T2_D' : [[13, 15, 12, 14], [15, 19, 18, 14], [13, 14, 16, 14], [14, 12, 15, 12], [12, 11, 17, 19]],
             'supply_capacities' : [186, 186, 281, 295],
             'demand_quantities' : [281, 154, 180, 311]}

nodes = {'no_of_supply_nodes' : 4,
        'no_of_first_layer_transshipment_nodes' : 2,
        'no_of_second_layer_transshipment_nodes' : 5,
        'no_of_demand_nodes' : 4}

# Problem
def main_lp():
    prob = pulp.LpProblem("Multi_Layer_Transshipment_Problem", pulp.LpMinimize)

    # Decision Variables
    x_s_t1 = pulp.LpVariable.dicts("x_s_t1", [(i, j) for i in range(4) for j in range(2)], lowBound=0, cat="Continuous")
    x_t1_t2 = pulp.LpVariable.dicts("x_t1_t2", [(j, k) for j in range(2) for k in range(5)], lowBound=0, cat="Continuous")
    x_t2_d = pulp.LpVariable.dicts("x_t2_d", [(k, l) for k in range(5) for l in range(4)], lowBound=0, cat="Continuous")

    # Objective Function
    prob += (
        pulp.lpSum(main_dict['c_S_T1'][i][j] * x_s_t1[i, j] for i in range(4) for j in range(2)) +
        pulp.lpSum(main_dict['c_T1_T2'][j][k] * x_t1_t2[j, k] for j in range(2) for k in range(5)) +
        pulp.lpSum(main_dict['c_T2_D'][k][l] * x_t2_d[k, l] for k in range(5) for l in range(4))
    )

    # Constraints
    for i in range(4):
        prob += pulp.lpSum(x_s_t1[i, j] for j in range(2)) <= main_dict['supply_capacities'][i]

    for j in range(2):
        prob += pulp.lpSum(x_s_t1[i, j] for i in range(4)) == pulp.lpSum(x_t1_t2[j, k] for k in range(5))

    for k in range(5):
        prob += pulp.lpSum(x_t1_t2[j, k] for j in range(2)) == pulp.lpSum(x_t2_d[k, l] for l in range(4))

    for l in range(4):
        prob += pulp.lpSum(x_t2_d[k, l] for k in range(5)) >= main_dict['demand_quantities'][l]

    #Solve
    prob.solve()

    # Results
    print("Status:", pulp.LpStatus[prob.status])
    print("Objective Value (Total Cost):", pulp.value(prob.objective))
    for v in prob.variables():
        if v.varValue > 0:
            print(v.name, "=", v.varValue)
    return prob.status



