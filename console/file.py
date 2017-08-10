import scipy.stats as sct

#0.908789   40    1.5   -> 42.000002
#NORM.INV(A2,A3,A4)   Inverse of the normal cumulative distribution for the terms above (42)   42.000002



"""
#d. how much top most 5% expensive house cost at least? or find x where P(X>=x) = 0.05
sct.norm.isf(q=0.05,loc=60,scale=40)

#e. how much top most 5% cheapest house cost at least? or find x where P(X<=x) = 0.05
sct.norm.ppf(q=0.05,loc=60,scale=40)
"""

import random

mean = 129.427211155379
stdv = 16.8367878228366
start_pice = 156.39

def test():
    meow = start_pice
    for tw in range(18):
        devi = stdv * meow / mean
        meow = sct.norm.ppf(random.random() ,meow, devi  )
        #print(meow)
    return meow


cnt_out3 = 0
cnt_drop = 0
for i in range(1000):
    simul = test()
    pattern = ( simul - start_pice ) / stdv

    if pattern > 3 or pattern < -3:
        cnt_out3 += 1
    if simul < start_pice:
        cnt_drop += 1

print(cnt_out3)
print(cnt_drop)

















