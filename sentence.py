import pickle
import math
import csv
from collections import Counter
from scipy import linalg
from numpy import c_, exp, log, inf, NaN, sqrt
import numpy
import random

import sys

reload(sys)
sys.setdefaultencoding('latin-1')

def gen_tri_sentence(prev1_word,prev2_word, unique_words,unigram, bigram,trigram):
    unique_words = list(unique_words)
    unique_words.remove("<s>")
    if prev1_word == "</s>":
        return "<s>"
    prob = numpy.zeros(len(unique_words))
    probt = numpy.zeros(len(unique_words))
    probb =numpy.zeros(len(unique_words))
    probu = numpy.zeros(len(unique_words))
    punc = [".",",","$","#","%","''", ":",";"]
    for (cnt,word) in enumerate(unique_words):
	if word not in punc:
	        #print(word)
        	triword = prev1_word + " " + prev2_word + " " + word
        	biword = prev2_word + " " + word
        	probt[cnt] = trigram[triword]
        	probb[cnt] = bigram[biword]
        	probu[cnt] = unigram[word]
        	
    totalt = sum(probt)
    totalb = sum(probb)
    totalu = sum(probu)
    if totalt!=0:
        probt = [x /totalt for x in probt]    
        #print("Total Probabt = ", prev1_word, sum(prob), len(unique_words))
        arr = numpy.random.choice(range(len(unique_words)), 1, p= probt)
    
    elif totalb!=0:
        probb = [x /totalb for x in probb]    
        #print("Total Probabb = ", prev1_word, sum(probb), len(unique_words))
        arr = numpy.random.choice(range(len(unique_words)), 1, p= probb)
    else:
        probu = [x /totalu for x in probu]    
        #print("Total Probabu = ", prev1_word, sum(probu), len(unique_words))
        arr = numpy.random.choice(range(len(unique_words)), 1, p= probu)
       
    #print(arr[0])
    word = unique_words[arr[0]]
    return word
        
        

def generate(ext):
          
    pickle_in = open(ext+"unique_wd.pickle","rb")
    unique_words = pickle.load(pickle_in)
    pickle_in.close()
    pickle_in = open(ext+"continuation_dic.pickle","rb")
    continuation = pickle.load(pickle_in)
    pickle_in.close()
    pickle_in = open(ext+"uni_dic.pickle","rb")
    unigram = pickle.load(pickle_in)
    pickle_in.close()
    pickle_in = open(ext+"bi_dic.pickle","rb")
    bigram = pickle.load(pickle_in)
    pickle_in.close()
    pickle_in = open(ext+"tri_dic.pickle","rb")
    trigram = pickle.load(pickle_in)
    pickle_in.close()
    pickle_in = open(ext+"alpha_dic.pickle","rb")
    alpha = pickle.load(pickle_in)
    pickle_in.close()
    pickle_in = open(ext+"alphasum_dic.pickle","rb")
    alphasum = pickle.load(pickle_in)
    pickle_in.close()

    
    tr_cnt = sum(unigram.values())
    #print(unigram)
    prev1_word = "<s>"
    prev2_word = "<s>"
    sentence = ""
    for i in range(10):
        #word = get_word(prev_word,0.95,continuation,tr_cnt,unique_words,unigram, bigram)
        word = gen_tri_sentence(prev1_word,prev2_word,unique_words,unigram, bigram,trigram)
        #print(word, " ")
        prev1_word = prev2_word
        prev2_word = word
        sentence = sentence + word + " "
        #print(i)
    print(sentence)
        
generate("D12")

