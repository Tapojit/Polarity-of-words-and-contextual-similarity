from __future__ import division
import sys,json,math
import os
import numpy as np
from math import sqrt
from _collections import defaultdict
import operator
import numpy as np

def load_word2vec(filename):
    # Returns a dict containing a {word: numpy array for a dense word vector} mapping.
    # It loads everything into memory.
    
    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):
    # Returns a dict containing a {word: contextcount} mapping.
    # It loads everything into memory.

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def dict_dotprod(dict_vec1, dict_vec2):
    smaller = dict_vec1 if len(dict_vec1)<len(dict_vec2) else dict_vec2  # BUGFIXED 20151012
    total = 0
    for key in smaller.iterkeys():
        total += dict_vec1.get(key,0) * dict_vec2.get(key,0)
    return total
def cos_sim(bow, word_1, word_2):
    w1_vec=bow[word_1]
    w2_vec=bow[word_2]
    
    dotprod=dict_dotprod(w1_vec, w2_vec)
    
    w1_pow_sum=0
    w2_pow_sum=0
    for keys in w1_vec.iterkeys():
        w1_pow_sum+=pow(w1_vec.get(keys),2)
    for keys in w2_vec.iterkeys():
        w2_pow_sum+=pow(w2_vec.get(keys),2)
    similarity=dotprod/(sqrt(w1_pow_sum)*sqrt(w2_pow_sum))
    return similarity




def cos_sim_word2vec(d1,word_1,word_2):
    w1_vec=d1[word_1]
    w2_vec=d1[word_2]
    
    dotprod=np.dot(w1_vec,w2_vec)
    
    w1_pow_sum=sum(np.square(w1_vec))
    w2_pow_sum=sum(np.square(w2_vec))
    
    similarity=dotprod/(sqrt(w1_pow_sum)*sqrt(w2_pow_sum))
    
    return similarity
      

def stream_contexts(filename):
    # Streams through (word, countextcount) pairs.
    # Does NOT load everything at once.
    # This is a Python generator, not a normal function.
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict
        
        
def king_queen_analogy(word1, word2, word3):
    data=load_word2vec("nyt_word2vec.4k")
    v_w1=data[word1]
    v_w2=data[word2]
    v_w3=data[word3]
    v_diff=np.add(np.subtract(v_w1,v_w2),v_w3)
    cos_sim_dict=defaultdict(float)
    for word in data.keys():
        dotprod=np.dot(data[word],v_diff)
        w1_pow_sum=sum(np.square(data[word]))
        w2_pow_sum=sum(np.square(v_diff))
        cos_sim_dict[word]=dotprod/(sqrt(w1_pow_sum)*sqrt(w2_pow_sum))
    return cos_sim_dict



def stream_cos_sim_calc(target_word):
    data=stream_contexts("nytcounts.4k")
    wordvec_tmap={}
    cos_sim_d=defaultdict(float)
    for word, ccdict in data:
        if target_word==word:
            wordvec_tmap=ccdict
            break
    data=stream_contexts("nytcounts.4k")
    for word, ccdict in data:
        if word!=target_word:
            data2={}
            data2[word]=ccdict
            data2[target_word]=wordvec_tmap
            cos_sim_d[word]=cos_sim(data2,word,target_word)
    return cos_sim_d


def stream_cos_sim_calc_word2vec(target_word):
    data=load_word2vec("nyt_word2vec.4k")
    wordvec_t=data[target_word];
    cos_sim_d=defaultdict(float)
    
    for word in data.keys():
        if word!=target_word:
            data2={}
            data2[word]=data[word]
            data2[target_word]=wordvec_t
            
            cos_sim_d[word]=cos_sim_word2vec(data2, word, target_word)
    return cos_sim_d


    
    
    
    
     