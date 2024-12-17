from main import *

#Decreasing shipment cost of supply node 0 to transshipment node 1_1 by 9
main_dict['c_S_T1'][0][1] -= 9

main_lp()

