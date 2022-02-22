from itertools import combinations
import json
import time
import copy
import numpy as np

def calc_cos(dists, index):
    # cos(dists[index]の対角)
    return (dists[(index + 2) % 3]**2 + dists[(index + 1) % 3]**2 - dists[index]**2)/(2 * dists[(index + 2) % 3] * dists[(index + 1) % 3])

def normalize_list(list_):
    max_ = 0
    for i in list_:
        max_ = max(np.max(list_), max_)
    return list_/max_

def calc_dist(x,y,ord):
    return np.linalg.norm(x-y,ord=ord)

def keymaker(ind0,ind1,ind2):
    return [[ind1  + 'to' + ind2, ind2  + 'to' + ind1],[ind0  + 'to' + ind1, ind1  + 'to' + ind0], [ind0  + 'to' + ind2, ind2  + 'to' + ind0]]

with open('F_G_datas\\img_avg_dist.json', mode = 'r') as f:
    img_dists = json.load(f)

# dist_v_testは生成データをパラレルデータで距離をはかった平均
# distは元データをパラレルデータで距離をはかった平均
# with open('pytorch-StarGAN-VC2-master\\dist_v_test.json', mode = 'r') as f:
with open('for_voice\\dist.json', mode = 'r') as f:
    voice_dists = json.load(f)

with open('F_G_datas\\img_F_or_M.json', mode='r') as f:
    img_labels = json.load(f)

voice_labels = ['SF1', 'SF2', 'TM1', 'TM2']
# 基準にするデータセットのラベル
v_0 =voice_labels[0]

temp3 = [1,2,3]
temp4 = list(range(4))
# 対応した辺を利用していることを確かにする
# タプルのリストが作成される
cor3 = list(combinations(temp3, 2))
cor4 = list(combinations(temp4, 2))
cor4_3 = list(combinations(temp4, 3))

targets = ['0', '0', '0']

# ラベルの確認
img_keys = img_dists.keys()
voice_keys = voice_dists.keys()

print("---img_keys---")
for i in img_keys:
    print(i)

print("---voice_keys---")
for i in voice_keys:
    print(i)

Fs = img_labels["Fs"]
Ms = img_labels["Ms"]
res = list(combinations(Fs, 2))

# 1.距離スケール&一点基準　用
cos_cri = []
v_d_cri = []
for i0,i1 in cor3:
    ds = []
    ds.append(voice_dists[voice_labels[i0] + 'to' + voice_labels[i1]])
    ds.append(voice_dists[v_0 + 'to' + voice_labels[i0]])
    ds.append(voice_dists[v_0 + 'to' + voice_labels[i1]])
    cos_cri.append(calc_cos(ds, 0))
    v_d_cri.append(ds)
v_d_cri = normalize_list(v_d_cri)
print(v_d_cri, cos_cri)

# 全点基準　用
only_cos_cri = []
for i0, i1, i2 in cor4_3:
    lab0, lab1, lab2 = voice_labels[i0], voice_labels[i1], voice_labels[i2]
    ds = []
    ds.append(voice_dists[lab0 + 'to' + lab1])
    ds.append(voice_dists[lab0 + 'to' + lab2])
    ds.append(voice_dists[lab1 + 'to' + lab2])
    only_cos_cri.append([calc_cos(ds, i) for i in range(3)])

# 基準にするデータセットのラベル
i_0 = ""
                
mycriteria = dict()

# 1.距離スケール&一点基準
# for i in range(len(Ms)):
#     Ms_t = copy.deepcopy(Ms)
#     i_0 = Ms_t.pop(i)
#     for j in Ms_t:
#         for k,l in res:
#             li = [i_0, j, k, l]
#             im_ds = []
#             coss = []
#             for t1,t2 in cor3:
#                 ds = []
#                 keys = keymaker(i_0, li[t1], li[t2])
#                 if keys[0][0] in img_keys:
#                     ds.append(img_dists[keys[0][0]])
#                 else:
#                     ds.append(img_dists[keys[0][1]])
#                 if keys[1][0] in img_keys:
#                     ds.append(img_dists[keys[1][0]])
#                 else:
#                     ds.append(img_dists[keys[1][1]])
#                 if keys[2][0] in img_keys:
#                     ds.append(img_dists[keys[2][0]])
#                 else:
#                     ds.append(img_dists[keys[2][1]])
#                 coss.append(calc_cos(ds, 0))
#                 im_ds.append(ds)
#             im_ds = normalize_list(im_ds)
#             print(f'--difference of {voice_labels} and {li} is--')
#             print(calc_dist(v_d_cri, im_ds, ord=1) + calc_dist(np.asarray(cos_cri),np.asarray(coss), ord=2))
#             mycriteria[f'--difference of {voice_labels} and {li} [in my criteria]--'] = calc_dist(v_d_cri, im_ds, ord=1) + calc_dist(np.asarray(cos_cri),np.asarray(coss), ord=2)

# with open('temp_result.json', mode='w') as f:
#     json.dump(mycriteria, f)

# 2.全点基準@combinations
# permutationsなら全探索できるが時間がかかる
# t_Fs = copy.deepcopy(Fs)
# Fs.extend(Ms)
# dists2 = []
# mycriteria2 = dict()
# for labels in combinations(Fs, 4):
#     only_coss = []
#     for i0, i1, i2 in cor4_3:
#         lab0, lab1, lab2 = labels[i0], labels[i1], labels[i2]
#         ds = []
#         keys = keymaker(labels[i0], labels[i1], labels[i2])
#         if keys[0][0] in img_keys:
#             ds.append(img_dists[keys[0][0]])
#         else:
#             ds.append(img_dists[keys[0][1]])
#         if keys[1][0] in img_keys:
#             ds.append(img_dists[keys[1][0]])
#         else:
#             ds.append(img_dists[keys[1][1]])
#         if keys[2][0] in img_keys:
#             ds.append(img_dists[keys[2][0]])
#         else:
#             ds.append(img_dists[keys[2][1]])
#         only_coss.append([calc_cos(ds, i) for i in range(3)])
#     t_dist = calc_dist(np.asarray(only_cos_cri), np.asarray(only_coss), ord=1)
#     dists2.append(t_dist)
#     # print(f"--difference of {voice_labels} and {labels} is {t_dist} [in my criteria2]--")
#     mycriteria2['to' + ''.join([i for i in labels])] = t_dist
# print(f"max;{np.max(dists2)}, avg:{np.average(dists2)}, min:{np.min(dists2)}")
# Fs = t_Fs
# with open('dist_img_to_vtest.json', mode = 'r') as f:
#     json.dump(mycriteria2, f)

# 男女固定
dists3 = []
mycriteria3 = dict()
for label_f in combinations(Fs, 2):
    for label_m in combinations(Ms, 2):
        Only_coss = []
        labels = [label_f[0], label_f[1], label_m[0], label_m[1]]
        for i0, i1, i2 in cor4_3:
            lab0, lab1, lab2 = labels[i0], labels[i1], labels[i2]
            ds = []
            keys = keymaker(labels[i0], labels[i1], labels[i2])
            if keys[0][0] in img_keys:
                ds.append(img_dists[keys[0][0]])
            else:
                ds.append(img_dists[keys[0][1]])
            if keys[1][0] in img_keys:
                ds.append(img_dists[keys[1][0]])
            else:
                ds.append(img_dists[keys[1][1]])
            if keys[2][0] in img_keys:
                ds.append(img_dists[keys[2][0]])
            else:
                ds.append(img_dists[keys[2][1]])
            Only_coss.append([calc_cos(ds, i) for i in range(3)])
        t_dist = calc_dist(np.asarray(only_cos_cri), np.asarray(Only_coss), ord=1)
        dists3.append(t_dist)
        print(f"--difference of {voice_labels} and {labels} is {t_dist} [in my criteria2]--")
        mycriteria3['to' + ''.join([i for i in labels])] = t_dist
print(f"max;{np.max(dists3)}, avg:{np.average(dists3)}, min:{np.min(dists3)}, var:{np.var(dists3)}")

# with open('dist_img_to_vtest.json', mode = 'w') as f:
# with open('dist_img_to_vtrain.json', mode = 'w') as f:
#     json.dump(mycriteria3, f)