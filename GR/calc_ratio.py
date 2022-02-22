from itertools import combinations
import json
import time
import copy
import numpy as np
with open('F_G_datas\\dist_img_to_vtest.json', mode = 'r') as f:
    dist_test = json.load(f)

with open('F_G_datas\\dist_img_to_vtrain.json', mode = 'r') as f:
    dist_train = json.load(f)

temp = []
for_s = dict()
for i in dist_test.keys():
    print("---",i,"---")
    print(dist_test[i]/dist_train[i])
    temp.append(dist_test[i]/dist_train[i])
    if temp[-1] > 2.2:
        print("\n\n\n\n\n\n\n\n\n", i, dist_test[i], dist_train[i], "\n\n\n\n\n\n\n\n")
    #  to1757378236996568 1.5228570699219957 0.6791549093716863だった
    for_s[i] = temp[-1]

print(np.average(temp), np.max(temp), np.min(temp), np.var(temp))

with open('ratio.json', mode='w') as f:
    json.dump(for_s, f)