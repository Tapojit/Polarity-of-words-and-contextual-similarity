from __future__ import division
from collections import defaultdict
import pickle
import os
import random
from math import log
from ecdsa.ecdsa import __main__

PATH_TO_DATA = "tweets.txt"
POS_SEED=["good", "nice", "love", "excellent", "fortunate", "correct", "superior"]
NEG_SEED=["bad", "nasty", "poor", "hate", "unfortunate", "wrong", "inferior"]
def tokenizer():
    bow=defaultdict(float);
    with open(PATH_TO_DATA, 'r') as doc:
        content=doc.read()
    tokens=content.split();
    tokens_lc=map(lambda y: y.lower(), tokens)
    for y in tokens_lc:
        bow[y]+=1.0
    return bow       

def polarity_calc(filter_500=False):
    count=0
    bow=tokenizer()
    w_pos=defaultdict(float)
    w_neg=defaultdict(float)
    polarity=defaultdict(float)
    pos_word_count=0
    neg_word_count=0
    N=sum(bow.values())
    for keys in bow.keys():
        if (keys in POS_SEED):
            pos_word_count+=bow[keys]
        elif (keys in NEG_SEED):
            neg_word_count+=bow[keys]
    for line in open(PATH_TO_DATA):
        count+=1
        tokens=line.split()
        tokens_lc=map(lambda y: y.lower(), tokens)
        for t in range(len(tokens_lc)):
            if tokens_lc[t] in POS_SEED:
                
                for t2 in tokens_lc[0:t]:
                    if(t2[0]!='@' and t2[0]!='#' and (t2 not in POS_SEED and t2 not in NEG_SEED)):
                        w_pos[t2]+=1.0
                for t2 in tokens_lc[t+1:]:
                    if(t2[0]!='@' and t2[0]!='#' and (t2 not in POS_SEED and t2 not in NEG_SEED)):
                        w_pos[t2]+=1.0
            elif tokens_lc[t] in NEG_SEED:
                for t2 in tokens_lc[0:t]:
                    if(t2[0]!='@' and t2[0]!='#' and (t2 not in POS_SEED and t2 not in NEG_SEED)):
                        w_neg[t2]+=1.0
                for t2 in tokens_lc[t+1:]:
                    if(t2[0]!='@' and t2[0]!='#' and (t2 not in POS_SEED and t2 not in NEG_SEED)):
                        w_neg[t2]+=1.0
    if(filter_500==True):
        for keys in bow.keys():
            if(keys not in POS_SEED and keys not in NEG_SEED and keys[0]!='@' and keys[0]!='#'and bow[keys]<500):
                PMI_pos=(w_pos[keys]/N)/((pos_word_count/N)*(bow[keys]/N))
                PMI_neg=(w_neg[keys]/N)/((neg_word_count/N)*(bow[keys]/N))
                
                if PMI_neg==0 and PMI_pos==0:
                    polarity[keys]=0
                elif PMI_pos==0:
                    
                    if log(PMI_neg,2)<0:
                        polarity[keys]=log(PMI_neg,2)
                    else:
                        polarity[keys]=-log(PMI_neg,2)
                elif PMI_neg==0:
                    polarity[keys]=abs(log(PMI_pos,2))
    else:
        for keys in bow.keys():
            if(keys not in POS_SEED and keys not in NEG_SEED and keys[0]!='@' and keys[0]!='#'):
                PMI_pos=(w_pos[keys]/N)/((pos_word_count/N)*(bow[keys]/N))
                PMI_neg=(w_neg[keys]/N)/((neg_word_count/N)*(bow[keys]/N))
                
                if PMI_neg==0 and PMI_pos==0:
                    polarity[keys]=0
                elif PMI_pos==0:
                    
                    if log(PMI_neg,2)<0:
                        polarity[keys]=log(PMI_neg,2)
                    else:
                        polarity[keys]=-log(PMI_neg,2)
                elif PMI_neg==0:
                    polarity[keys]=abs(log(PMI_pos,2))
                    
    return polarity
        

if __name__=='__main__':
    
    polarity_calc()