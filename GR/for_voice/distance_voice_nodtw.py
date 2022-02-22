import os
import re
import glob
import pathlib

train_dir = '.\\data\\spk\\*'
test_dir = '.\\data\\spk_test\\*'

train_dirs = glob.glob(train_dir)

wav_files = []

for p in pathlib.Path(train_dirs[0]).glob('*.wav'):
    wav_files.append(p.name)

wav_sets = set(wav_files)

for i in range(1,len(train_dirs)):
    wav_files = []
    for p in pathlib.Path(train_dirs[i]).glob('*.wav'):
        wav_files.append(p.name)
    wav_sets = wav_sets & set(wav_files)

wav_list = list(wav_sets)
wav_list.sort()
print(wav_list, len(wav_list))

# for dir,i in enumerate(train_dirs):
#     tmp = set(glob.glob(dir + "/*.wav"))
#     wav_files = 

# -*- coding: utf-8 -*-
import os
import sys
import librosa
import numpy as np
import pyworld
import pysptk
from nnmnkwii.metrics import melcd

# sr = 22050
sr = 16000 # sample rate of VCC2016
FRAME_PERIOD = 5.0 #default 5.0
# alpha = 0.65  # commonly used at 22050 Hz
alpha = 0.42 # used at 16kHz
fft_size = 512 #default 512
mcep_dim = 34 #default 34

# # sample_rateは使う予定なし
# wav1, sample_rate1 = librosa.load(sys.argv[1], sr=sr, mono=True)
# wav2, sample_rate2 = librosa.load(sys.argv[2], sr=sr, mono=True)

# # Use WORLD vocoder to spectral envelope
# _, sp1, _ = pyworld.wav2world(wav1.astype(np.double), fs=sr, frame_period=FRAME_PERIOD, fft_size=fft_size)
# # Extract MCEP features
# mgc1 = pysptk.sptk.mcep(sp1, alpha=alpha, maxiter=0, etype=1, eps=1.0E-8, min_det=0.0, itype=3)
# # Use WORLD vocoder to spectral envelope
# _, sp2, _ = pyworld.wav2world(wav2.astype(np.double), fs=sr,frame_period=FRAME_PERIOD, fft_size=fft_size)
# # Extract MCEP features
# mgc2 = pysptk.sptk.mcep(sp2, alpha=alpha, maxiter=0, etype=1, eps=1.0E-8, min_det=0.0, itype=3)

# ref_frame_no = len(mgc1)

# min_cost, wp = librosa.sequence.dtw(mgc1[:, 1:].T, mgc2[:, 1:].T)

# result = melcd(mgc1[wp[:,0]], mgc2[wp[:,1]] , lengths=None)

# print(result)
with open('dist_dtw.txt', mode = 'w') as f:
    for i in range(len(train_dirs)):
        for j in range(i+1,len(train_dirs)):
            dist = []
            for k in wav_list:
                wav1, _ = librosa.load(train_dirs[i] + "\\" + k, sr = sr)
                wav2, _ = librosa.load(train_dirs[j] + "\\" + k, sr = sr)

                wav1 = wav1.astype(np.float64)
                wav2 = wav2.astype(np.float64)

                f0_1, timeaxis_1 = pyworld.harvest(wav1[wp[:,0]], sr, frame_period = FRAME_PERIOD, f0_floor=71.0, f0_ceil=800.0)
                sp1 = pyworld.cheaptrick(wav1[wp[:,0]], f0_1, timeaxis_1, sr)

                f0_2, timeaxis_2 = pyworld.harvest(wav2[wp[:,1]], sr, frame_period = FRAME_PERIOD, f0_floor=71.0, f0_ceil=800.0)
                sp2 = pyworld.cheaptrick(wav2[wp[:,1]], f0_2, timeaxis_2, sr)

                coded_sp_1 = pyworld.code_spectral_envelope(sp1, sr, 24)
                coded_sp_2 = pyworld.code_spectral_envelope(sp2, sr, 24)

                # result = melcd(coded_sp_1, coded_sp_2, lengths = None)

                # _, sp1, _ = pyworld.wav2world(wav1.astype(np.double), fs = sr, frame_period = FRAME_PERIOD, fft_size = fft_size)
                # mgc1 = pysptk.sptk.mcep(sp1, alpha = alpha, maxiter = 0, etype = 1, eps = 1.0e-8, min_det = 0.0, itype = 3)

                # _, sp2, _ = pyworld.wav2world(wav2.astype(np.double), fs = sr, frame_period = FRAME_PERIOD, fft_size = fft_size)
                # mgc2 = pysptk.sptk.mcep(sp2, alpha = alpha, maxiter = 0, etype = 1, eps = 1.0E-8, min_det = 0.0, itype = 3)
                
                # ref_frame_no = len(mgc1)
                
                # min_cost, wp = librosa.sequence.dtw(mgc1[:, 1:].T, mgc2[:, 1:].T)
                
                # result = melcd(mgc1[wp[:,0]], mgc2[wp[:,1]] , lengths=None)
                print(f"{i}_{k} to {j}_{k} distance is {result}")
                dist.append(result)
            print("average of {} to {} = {}".format(train_dirs[i], train_dirs[j], np.average(dist)))
            print("varriance of {} to {} = {}".format(train_dirs[i], train_dirs[j], np.var(dist)))
            print("max = {} min = {}".format(np.max(dist), np.min(dist))) 
            f.write("average of {} to {} = {}, ".format(train_dirs[i], train_dirs[j], np.average(dist)))
            f.write("varriance of {} to {} = {}".format(train_dirs[i], train_dirs[j], np.var(dist)))
            f.write("max = {} min = {}\n".format(np.max(dist), np.min(dist)))