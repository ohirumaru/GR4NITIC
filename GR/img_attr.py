# Celeb-A dataset's size is 178 * 218

import time
import numpy as np
import json
from PIL import Image

with open("F_G_datas\\image_indexs_mt_30.json", mode = 'r') as f:
    mydict = json.load(f)

def calc_dist(x,y):
    return np.linalg.norm(x-y)

with open("F_G_datas\\list_attr_celeba.txt", mode='r') as f:
    lines = f.readlines()

label = ['Female', "Male"]
# print(mydict)
print(lines[1].split(" "))
print(lines[1].split(" ")[20])
Ms = []
Fs = []
for k,v in mydict.items():
    print('--------',k,'--------')
    # for va in v:
    #     index = int(va[:-4])
    #     tmp = sum([i.split(" ") for i in lines[index+1].split("  ")], [])[21]
    #     print(label[(int(tmp) + 1)//2])
    index = int(v[0][:-4])
    tmp = sum([i.split(" ") for i in lines[index+1].split("  ")], [])[21]
    if k == '9152':
        # 性別のラベルがバラバラ、目視で確認したらFemaleだった
        Fs.append(k)
    elif label[(int(tmp) + 1)//2] == 'Male':
        Ms.append(k)
    else:
        Fs.append(k)

# label = dict()
# label["Fs"] = Fs
# label["Ms"] = Ms

# with open("F_G_datas\\img_F_or_M.json",mode="w") as f:
#     json.dump(label, f)

img_dists = dict()
img_dists_v = dict()
img_dists_min = dict()
img_dists_max = dict()

# FemaleとMale間のみ
# for i in Fs:
#     for j in Ms:
#         dist = []
#         # cnt = 0
#         for v1 in mydict[i]:
#             im_f = np.array(Image.open('img_align_celeba\\' + v1))
#             for v2 in mydict[j]:
#                 im_m = np.array(Image.open('img_align_celeba\\' + v2))
#                 # ここで距離を測る
#                 dist_tmp = calc_dist(im_f,im_m)
#                 print(f"dist {v1} to {v2} is {dist_tmp}")
#                 dist.append(dist_tmp)
#                 # cnt += 1

#         dist_avg = np.average(dist)
#         dist_var = np.var(dist)
#         dist_min = np.min(dist)
#         dist_max = np.max(dist)
#         print('dist of',i,'to',j,'=',dist_avg)
#         print(f'avg: {dist_avg}, var: {dist_var}, min: {dist_min}, max: {dist_max}')
#         img_dists[v1 + 'to' + v2] = dist_avg
#         img_dists_v[v1 + 'to' + v2] = dist_var
#         img_dists_max[v1 + 'to' + v2] = dist_max
#         img_dists_min[v1 + 'to' + v2] = dist_min



# with open('F_G_datas\\img_dist.json', mode = 'w') as f:
#     json.dump(img_dists, f)
# with open('F_G_datas\\img_dist_v.json', mode = 'w') as f:
#     json.dump(img_dists_v, f)
# with open('F_G_datas\\img_dist_max.json', mode = 'w') as f:
#     json.dump(img_dists_max, f)
# with open('F_G_datas\\img_dist_min.json', mode = 'w') as f:
#     json.dump(img_dists_min, f)

from itertools import combinations
Fs.extend(Ms)
ne = combinations(Fs, 2)

# 全通り
# print(list(ne),Fs)
for i,j in ne:
    dist = []
    # cnt = 0
    for v1 in mydict[i]:
        im_f = np.array(Image.open('img_align_celeba\\' + v1))
        for v2 in mydict[j]:
            im_m = np.array(Image.open('img_align_celeba\\' + v2))
            # ここで距離を測る
            dist_tmp = calc_dist(im_f,im_m)
            # print(f"dist {v1} to {v2} is {dist_tmp}")
            dist.append(dist_tmp)
            # cnt += 1

    dist_avg = np.average(dist)
    dist_var = np.var(dist)
    dist_min = np.min(dist)
    dist_max = np.max(dist)
    print('dist of',i,'to',j,'=',dist_avg)
    print(f'avg: {dist_avg}, var: {dist_var}, min: {dist_min}, max: {dist_max}')
    img_dists[i + 'to' + j] = dist_avg
    img_dists_v[i + 'to' + j] = dist_var
    img_dists_max[i + 'to' + j] = dist_max
    img_dists_min[i + 'to' + j] = dist_min



with open('F_G_datas\\img_dist_con.json', mode = 'w') as f:
    json.dump(img_dists, f)
with open('F_G_datas\\img_dist_v_con.json', mode = 'w') as f:
    json.dump(img_dists_v, f)
with open('F_G_datas\\img_dist_max_con.json', mode = 'w') as f:
    json.dump(img_dists_max, f)
with open('F_G_datas\\img_dist_min_con.json', mode = 'w') as f:
    json.dump(img_dists_min, f)




# print('--------9152--------')
# for v in mydict['9152']:
#     # Image.open('img_align_celeba\\' + v).show()
#     index = int(v[:-4])
#     tmp = sum([i.split(" ") for i in lines[index+1].split("  ")], [])[21]
    
# for k, v in mydict.items():
#     for i in v:
#         im = np.array(Image.open('img_align_celeba\\'+i))

# 盾に足した時の平均も取りたい?
# 要するに、データセットの中心間の距離