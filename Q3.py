from main import main_lp, main_dict

#Supply node 0 can not ship to transshipment node 1_0
main_dict['c_S_T1'][0][0] = 100000

main_lp()


