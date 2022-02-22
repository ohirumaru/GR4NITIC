# use this program to convert .txt to .json
import json

with open("dist.txt", mode='r') as f:
    lines = f.readlines()

dist_avg = {}
for line in lines:
    temp = line.split(" ")
    dist_avg[temp[2][-3:] + temp[3] + temp[4][-3:]] = float(temp[6][:-1])

# print(dist_avg)
with open("dist.json", mode = 'w') as f:
    json.dump(dist_avg, f)
