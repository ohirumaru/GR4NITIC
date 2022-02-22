from itertools import combinations
import json
import time

def calc_cos(dists, index):
    # cos(dists[index]の対角)
    return (dists[(index + 2) % 3]**2 + dists[(index + 1) % 3]**2 - dists[index]**2)/(2 * dists[(index + 2) % 3] * dists[(index + 1) % 3])

with open('F_G_datas\\img_dist_con.json', mode = 'r') as f:
    img_dists = json.load(f)
with open('F_G_datas\\img_dist_v.json', mode = 'r') as f:
    img_dists_v = json.load(f)
with open('F_G_datas\\img_dist_max.json', mode = 'r') as f:
    img_dists_max = json.load(f)
with open('F_G_datas\\img_dist_min.json', mode = 'r') as f:
    img_dists_min = json.load(f)
with open('F_G_datas\\img_F_or_M.json', mode = 'r') as f:
    label = json.load(f)

l_F = [i for i in range(len(label["Fs"]))]
l_M = [i for i in range(len(label["Ms"]))]
# タプルのリストへ
c_F = list(combinations(l_F,2))
c_M = list(combinations(l_M,2))

targets = ['0', '0', '0']

# print(img_dists.keys())

for i_F,j_F in c_F:
    for i_M,j_M in c_M:
        F1, F2, M1, M2 = label["Fs"][i_F], label["Fs"][j_F], label["Ms"][i_M], label["Ms"][j_M]
        c_temp = list(combinations([F1,F2,M1,M2],3))
        for i in c_temp:
            c_twin = list(combinations(i, 2))
            dists = []
            for j,k in c_twin:
                dists.append(img_dists[j + 'to' + k])
            # ここで三つのdistからcosを求める
            # を求める
            targets[0] = list(set(i) ^ set([c_twin[0][0], c_twin[0][1]]))[0]
            targets[1] = list(set(i) ^ set([c_twin[1][0], c_twin[1][1]]))[0]
            targets[2] = list(set(i) ^ set([c_twin[2][0], c_twin[2][1]]))[0]
            print(f"cos∠ {targets[1]} {targets[0]} {targets[2]} = {calc_cos(dists, 0)}")
            print(f"cos∠ {targets[2]} {targets[1]} {targets[0]} = {calc_cos(dists, 1)}")
            print(f"cos∠ {targets[0]} {targets[2]} {targets[1]} = {calc_cos(dists, 2)}")


