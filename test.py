#test 

import numpy as np

n = 20
tab_ruban = np.array([None] * n)

Instruction = ["ALLER"]*(n-2) + ["ARRET"] + ["ARRET"]
tab_ruban[0]=("B", ">", Instruction[0])
tab_ruban[n-1] = ("X", ">", Instruction[n-1])


l = 0
thr = tab_ruban[l]


while (thr[2]!="ARRET"):
    thr = tab_ruban[l]
    if thr[2] == "ALLER" :
        if thr[1] == ">" :
            tab_ruban[l+1] = (thr[0], ">", Instruction[l])
            l = l + 1
        else :
            tab_ruban[l-1] = (thr[0], "<", Instruction[l])
            l = l - 1


print(tab_ruban)