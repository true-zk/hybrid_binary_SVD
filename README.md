# hybrid_binary_SVD
A Hybrid Binary Static Vulnerability Detection NN model. 

Decompile by retdec.

Use [SARD Juliet test suite](https://samate.nist.gov/SARD/test-suites/112) as c/c++ dataset

\*tip: *if u have no idea how to compile this dataset, can use [this one](https://github.com/arichardson/juliet-test-suite-c)*


---

# file tree:
 *There may some same files in different folders. BUT the **useful files** have been listed below. The other files are scraps when I do exp. I donot want del them for backup reason, though they are useless for u and may confuse u. Pardon me plz.*

## 1. decompile
-  *Decom_CWE.py* : main file for decompile bin files to dsm and dot files
- *scrap.py* : match num of dsm and dot files

## 2. w2v_cfg
- *main.py* : main 
- *dot2token.py* : gen token.txt from dot files to token_out folder
- *word2vec.py* : gen w2v.model from token.txt file to model_out folder

## 3. w2v_token
- *main.py* : main 
- *preextract.py* : from dsm file extract the target func (with vulnerability or corresponding good) from origin dsm file to extract_dsm
- *gensim_w2v_model.py* : gen w2v.model use extract_dsm to model_out folder

## 4. cfgdetect
- *main.ipynb* : load dataset && train&test cfg model
- *gendata_new.py* : gen dataset

## 5. tokendetect
- *main.ipynb* : load dataset && train&test token model
- *gendata.py* : gen dataset

## 6. hybrid-SVD
- *main_binary.ipynb* : load dataset && train&test hybrid model
- *gendata_binary.py* : gen dataset

## 7. exp_multi
- *hybrid_multi.ipynb* : hybrid model for multi CWE detection
- *cfg_multi.ipynb* : cfg model for multi CWE detection
- *token_multi.ipynb* : token model for multi CWE detection
- *all_multi.ipynb* : all three models above for backup reason

## 8. dataset
- *dataset for multi labels classification*
- *myplot.png* : the hist graph for the whole multi labels dataset, which decides 'height' of dsm input is 175.

---
# cite list
1. CFG static vulnerability detection model from [CFG_SVD](https://github.com/Snowfall99/CFG-SVD) some ref also in this repository.
   
    \*And this work has been published as :  [陈皓, 易平. 基于图神经网络的代码漏洞检测方法[J]. 网络与信息安全学报, 2021, 7(3): 37-45.](http://www.infocomm-journal.com/cjnis/CN/10.11959/j.issn.2096-109x.2021039)

2. Instruction2vec from paper : [Lee, Y.; Kwon, H.; Choi, S.-H.; Lim, S.-H.; Baek, S.H.; Park, K.-W. Instruction2vec: Efficient Preprocessor of Assembly Code to Detect Software Weakness with CNN. Appl. Sci. 2019, 9, 4086.](https://www.mdpi.com/2076-3417/9/19/4086)
3. TextCNN from paper : [Kim Y. Convolutional Neural Networks for Sentence Classification[J].](https://emnlp2014.org/papers/pdf/EMNLP2014181.pdf)
4. Attention for CNN from paper : [Woo S, Park J, Lee J Y, et al. Cbam: Convolutional block attention module[C]//Proceedings of the European conference on computer vision (ECCV). 2018: 3-19.](https://openaccess.thecvf.com/content_ECCV_2018/html/Sanghyun_Woo_Convolutional_Block_Attention_ECCV_2018_paper.html)
5. Word2vec from paper : [Church K W. Word2Vec[J]. Natural Language Engineering, 2017, 23(1): 155-162.](https://www.cambridge.org/core/journals/natural-language-engineering/article/word2vec/B84AE4446BD47F48847B4904F0B36E0B)
6. Why textCNN & instruction2vec can be used for SVD. And my token SVD model is from this paper : [Yan H, Luo S, Pan L, et al. HAN-BSVD: a hierarchical attention network for binary software vulnerability detection[J]. Computers & Security, 2021, 108: 102286.](https://www.sciencedirect.com/science/article/pii/S0167404821001103) 
   
   *I donot use the whole model from this paper. I think the Bi-GRU is a verbose module because the word2vec has been used to pre extract and embed dsm.

   *This paper's official model is not public. So I have no idea if my partial re-implementation is identical to the paper's. Hope it is.