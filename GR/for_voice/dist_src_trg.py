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

src_dir = '.\\data\\spk_test\\*'

trg_dir  = '.\\outputs\\results\\'

mydict = {
    "SF1":[],
    "SF2":[],
    "TM1":[],
    "TM2":[],
}

src_dirs = glob.glob(src_dir)

for i in ["SF1","SF2","TM1","TM2"]:
    for p in pathlib.Path(trg_dir).glob(i + '-' +  i + '*.wav'):
        mydict[i].append(p.name)
l = list(mydict.keys())

for i, k in enumerate(mydict.keys()):
    dist = []
    for v in mydict[k]:
        wav1, _ = librosa.load(trg_dir + "\\" + v)
        wav2, _ = librosa.load(src_dirs[i] + "\\" + v[18:])
        
        _, sp1, _ = pyworld.wav2world(wav1.astype(np.double), fs = sr, frame_period = FRAME_PERIOD, fft_size = fft_size)
        mgc1 = pysptk.sptk.mcep(sp1, alpha = alpha, maxiter = 0, etype = 1, eps = 1.0e-8, min_det = 0.0, itype = 3)

        _, sp2, _ = pyworld.wav2world(wav2.astype(np.double), fs = sr, frame_period = FRAME_PERIOD, fft_size = fft_size)
        mgc2 = pysptk.sptk.mcep(sp2, alpha = alpha, maxiter = 0, etype = 1, eps = 1.0E-8, min_det = 0.0, itype = 3)
        ref_frame_no = len(mgc1)
        min_cost, wp = librosa.sequence.dtw(mgc1[:, 1:].T, mgc2[:, 1:].T)
        
        result = melcd(mgc1[wp[:,0]], mgc2[wp[:,1]] , lengths=None)
        dist.append(result)
    print("average of src{} to trg{} = {}".format(src_dirs[i], k, np.average(dist)))
    print("varriance of src{} to trg{} = {}".format(src_dirs[i], k, np.var(dist)))
    print("max = {} min = {}".format(np.max(dist), np.min(dist)))
    with open('dist_srt_trg.txt', mode = 'a') as f:
        f.write("average of src{} to trg{} = {}, ".format(src_dirs[i], k, np.average(dist)))
        f.write("varriance of src{} to trg{} = {}".format(src_dirs[i], k, np.var(dist)))
        f.write("max = {} min = {}\n".format(np.max(dist), np.min(dist)))