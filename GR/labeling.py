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

label = dict()
label["Fs"] = Fs
label["Ms"] = Ms

with open("F_G_datas\\img_F_or_M.json",mode="w") as f:
    json.dump(label, f)