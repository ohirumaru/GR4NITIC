import json
mydict = dict()
for i in range(10177):
    mydict[str(i+1)] = []
with open("F_G_datas\\identity_CelebA.txt","r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.split()

        mydict[line[1]].append(line[0])

index = dict()
for i in range(35):
    index[i+1] = []

for i in range(10177):
    # print(f"number of included identity{i+1}-images: {len(mydict[str(i+1)])}")
    index[len(mydict[str(i+1)])].append(str(i+1))

index = sorted(index.items())
index = index[30:]
# with open('images_mt_30.txt', mode = 'w') as f:
#     for i in range(30,35):
#         if i == 32:
#             pass
#         else:
#             f.write(f"{index[i][0]}: {index[i][1]}\n")
k = []
for i in index:
    for j in i[1]:
        k.append(j)
        # lists = ['0']*i[0]

l = set(k)
m = set([str(i) for i in range(1,10178)])
n = l^m

for i in n:
    mydict.pop(i)

with open('F_G_datas\\image_indexs_mt_30.json', mode = 'w') as f:
    json.dump(mydict, f)
