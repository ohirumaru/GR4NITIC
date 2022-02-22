"""
TODO:
*同じラベルに変換したときの距離を調べる
*変換元のラベルと距離の相関を調べる
"""

# -*- coding: utf-8 -*-
import os
import sys
import librosa
import numpy as np
import pyworld
import pysptk
from nnmnkwii.metrics import melcd
import re
import glob
import pathlib

sr = 16000 # sample rate of VCC2016
FRAME_PERIOD = 5.0 
alpha = 0.42 # used at 16kHz
fft_size = 512 
mcep_dim = 34

# 1つあたり54こ*4
dir  = '.\\outputs\\results\\'

mydict = {
    "SF1":[],
    "SF2":[],
    "TM1":[],
    "TM2":[],
}
for i in ["SF1","SF2","TM1","TM2"]:
    for p in pathlib.Path(dir).glob(i+'*.wav'):
        mydict[i].append(p.name)

l = list(mydict.keys())

wavs = {
    "SF1":[],
    "SF2":[],
    "TM1":[],
    "TM2":[],
}

for k, v in mydict.items():
    for v1 in v:
        wavs[v1[4:7]].append(v1)
        
import itertools

p = [0,1,2,3]

p = list(itertools.combinations(p, 2))

dist = []
cnt = 0

for i in range(len(l)):
    for j in range(i, len(l)):
        for m,n in p:
            for w1,w2 in zip(mydict[l[i]][m*54:(m+1) * 54], mydict[l[j]][n * 54:(n+1) * 54]):
                cnt += 1
                wav1, _ = librosa.load(dir + w1)
                wav2, _ = librosa.load(dir + w2)
                _, sp1, _ = pyworld.wav2world(wav1.astype(np.double), fs = sr, frame_period = FRAME_PERIOD, fft_size = fft_size)
                mgc1 = pysptk.sptk.mcep(sp1, alpha = alpha, maxiter = 0, etype = 1, eps = 1.0e-8, min_det = 0.0, itype = 3)

                _, sp2, _ = pyworld.wav2world(wav2.astype(np.double), fs = sr, frame_period = FRAME_PERIOD, fft_size = fft_size)
                mgc2 = pysptk.sptk.mcep(sp2, alpha = alpha, maxiter = 0, etype = 1, eps = 1.0E-8, min_det = 0.0, itype = 3)
                
                ref_frame_no = len(mgc1)
                
                min_cost, wp = librosa.sequence.dtw(mgc1[:, 1:].T, mgc2[:, 1:].T)
                
                result = melcd(mgc1[wp[:,0]], mgc2[wp[:,1]] , lengths=None)
                
                dist.append(result)
                if cnt == 54:
                    print("average of {}_{} to {}_{} = {}".format(l[i], w1[4:7], l[j], w2[4:7], np.average(dist)))
                    dist = []
                    cnt = 0


# for i in range(len(l)):
#     for j in range(i+1 ,len(l)):
#         dist = []
#         cnt = 0
#         for w1,w2 in zip(mydict[l[i]][i*54:(i+1) * 54], mydict[l[i]][j * 54:(j+1) * 54]):
#             cnt += 1
#             wav1, _ = librosa.load(dir + w1)
#             wav2, _ = librosa.load(dir + w2)
#             _, sp1, _ = pyworld.wav2world(wav1.astype(np.double), fs = sr, frame_period = FRAME_PERIOD, fft_size = fft_size)
#             mgc1 = pysptk.sptk.mcep(sp1, alpha = alpha, maxiter = 0, etype = 1, eps = 1.0e-8, min_det = 0.0, itype = 3)

#             _, sp2, _ = pyworld.wav2world(wav2.astype(np.double), fs = sr, frame_period = FRAME_PERIOD, fft_size = fft_size)
#             mgc2 = pysptk.sptk.mcep(sp2, alpha = alpha, maxiter = 0, etype = 1, eps = 1.0E-8, min_det = 0.0, itype = 3)
            
#             ref_frame_no = len(mgc1)
            
#             min_cost, wp = librosa.sequence.dtw(mgc1[:, 1:].T, mgc2[:, 1:].T)
            
#             result = melcd(mgc1[wp[:,0]], mgc2[wp[:,1]] , lengths=None)
            
#             dist.append(result)
#             if cnt == 54:
#                 print("average of {}_{} to {}_{} = {}".format(l[i], w1[4:7], l[i], w2[4:7], np.average(dist)))
#                 dist = []
#                 cnt = 0
            
        # print("average of {} to {} = {}".format(l[i], l[j], np.average(dist)))
        # with open('dist_label_depend_test.txt', mode = 'a') as f:
        #     f.write("average of {} to {} = {}, ".format(l[i],l[j], np.average(dist)))
        #     f.write("varriance of {} to {} = {}".format(l[i],l[j], np.var(dist)))
        #     f.write("max = {} min = {}\n".format(np.max(dist), np.min(dist)))
        # for w1,w2 in zip(mydict[l[i]], mydict[l[j]]):
        #     cnt += 1
        #     wav1, _ = librosa.load(dir + w1)
        #     wav2, _ = librosa.load(dir + w2)
        #     _, sp1, _ = pyworld.wav2world(wav1.astype(np.double), fs = sr, frame_period = FRAME_PERIOD, fft_size = fft_size)
        #     mgc1 = pysptk.sptk.mcep(sp1, alpha = alpha, maxiter = 0, etype = 1, eps = 1.0e-8, min_det = 0.0, itype = 3)

        #     _, sp2, _ = pyworld.wav2world(wav2.astype(np.double), fs = sr, frame_period = FRAME_PERIOD, fft_size = fft_size)
        #     mgc2 = pysptk.sptk.mcep(sp2, alpha = alpha, maxiter = 0, etype = 1, eps = 1.0E-8, min_det = 0.0, itype = 3)
            
        #     ref_frame_no = len(mgc1)
            
        #     min_cost, wp = librosa.sequence.dtw(mgc1[:, 1:].T, mgc2[:, 1:].T)
            
        #     result = melcd(mgc1[wp[:,0]], mgc2[wp[:,1]] , lengths=None)
            
        #     dist.append(result)
        #     if cnt == 54:
        #         print("average of {}_{} to {}_{} = {}".format(l[i], w1[4:7], l[j], w2[4:7], np.average(dist)))
        #         dist = []
        #         cnt = 0
            
        # # print("average of {} to {} = {}".format(l[i], l[j], np.average(dist)))
        # # with open('dist_label_depend_test.txt', mode = 'a') as f:
        # #     f.write("average of {} to {} = {}, ".format(l[i],l[j], np.average(dist)))
        # #     f.write("varriance of {} to {} = {}".format(l[i],l[j], np.var(dist)))
        # #     f.write("max = {} min = {}\n".format(np.max(dist), np.min(dist)))