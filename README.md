# GR4NITIC
Graduation Research for The National Institute of Technology, Ibaraki College  
This account and repositry uses for MJ's GR only.  
I wrote a lot of the code on the spur of the moment, so I'll fix it later to make it more readable(I wrote this using DeepL.).  
If you want to execute these codes, you should place like below.

<pre>
└─GR
    │  
    ├─img_align_celeba
    ├─for_voice
    │  │ 
    |  ├─data
    │  └─outputs
    └─F_G_datas

</pre>
  
  
data is from [VCC2016 dataset](https://datashare.ed.ac.uk/handle/10283/2211), outputs is from [this repository's code](https://github.com/Oscarshu0719/pytorch-StarGAN-VC2), and img_align_celeba is from [CelebA dataset](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)

<br>

## Description
##### distance_voice.py
calculate MCD of train data
##### dist_test.py
calculate MCD of test data
##### dist_src_trg.py
calculate MCD between source data and target data
##### calc_gon.py
calculate cosine of image dataset
##### calc_gon_voice.py
calculate cosine of voice dataset and compare with image's value
##### calc_ratio.py
calculate ratio of cosine value
##### img_attr.py
divide image dataset into men and women and measure euclidian distance.(all combination)
##### img_avg_dist.py
calculate average of each label. after that, calculate euclidian distance.
##### img_process.py
find label which has more than 30 images

## acknowledgments
I couldn't write broken acknowledgments in the report. So, I wrote that here.  
First of all, I would like to express my deepest gratitude to "SHACHI" who developed "AI Kiritan" and got me interested in speech research.  
I would also like to thank "DeepL" for translating my poor Japanese into poor English, and for helping me with my transfer study, and Mr. H for discussing my research progress and keeping me motivated. I can't thank you enough.  
... And so on.
