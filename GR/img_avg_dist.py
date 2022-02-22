import time
import numpy as np
import json
from PIL import Image
from itertools import combinations

with open("F_G_datas\\image_indexs_mt_30.json", mode = 'r') as f:
    mydict = json.load(f)

with open("F_G_datas\\img_F_or_M.json",mode="r") as f:
    label = json.load(f)

with open("F_G_datas\\img_dist_v_con.json", mode = "r") as f:
    wow = json.load(f)

ne = label["Fs"]
ne.extend(label["Ms"])
ne = combinations(ne, 2)

def calc_dist(x,y):
    return np.linalg.norm(x-y)

img_dists = dict()
img_dists_v = dict()
img_dists_min = dict()
img_dists_max = dict()

for i,j in ne:
    dist = []
    v1_tot, v2_tot = [],[]
    for v1 in mydict[i]:
        im_f = np.array(Image.open('img_align_celeba\\' + v1))
        if v1_tot == []:
            v1_tot = im_f
        else:
            v1_tot += im_f
    for v2 in mydict[j]:
        im_m = np.array(Image.open('img_align_celeba\\' + v2))
        if v2_tot == []:
            v2_tot = im_m
        else:
            v2_tot += im_m
    # ここで距離を測る
    dist_tmp = calc_dist(v1_tot/len(mydict[i]),im_m/len(mydict[j]))
    # print(f"dist {v1} to {v2} is {dist_tmp}")
    dist.append(dist_tmp)

    # dist_avg = np.average(dist)
    # dist_var = np.var(dist)
    # dist_min = np.min(dist)
    # dist_max = np.max(dist)
    print('dist of',i,'to',j,'=',dist_tmp)
    # print(f'avg: {dist_avg}, var: {dist_var}, min: {dist_min}, max: {dist_max}')
    img_dists[i + 'to' + j] = dist_tmp
    # img_dists_v[i + 'to' + j] = dist_var
    # img_dists_max[i + 'to' + j] = dist_max
    # img_dists_min[i + 'to' + j] = dist_min

# from sklearn import preprocessing
# mm = preprocessing.MinMaxScaler()
def min_max(l):
    l_min = min(l)
    l_max = max(l)
    return [(i - l_min) / (l_max - l_min) for i in l]

img_ = min_max(list(img_dists.values()))
www = min_max(list(wow.values()))
print(f"varriance:{np.var(img_)}")
print(f"varriance:{np.var(www)}")

# with open('F_G_datas\\img_avg_dist.json', mode = 'w') as f:
#     json.dump(img_dists, f)