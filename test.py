import pickle
import math
import csv
from collections import Counter
from scipy import linalg
from numpy import c_, exp, log, inf, NaN, sqrt

import sys

reload(sys)
sys.setdefaultencoding('latin-1')



def alphav(beta, alpha,unique_words):
	alpha_v = dict((name,0) for name in unique_words)
	for word in unique_words:
		s_total = sum(alpha[word].values())
		l_total = len(alpha[word])
		if s_total!=0:
			alpha_v[word] = 1 - ((s_total - (s_total - l_total*beta))/float(s_total))
		else:
			alpha_v[word] = 1
	return alpha_v

def word_count(data):
    count = 0
	#data = list(data.split())
    count = len(data.split())
    return count

def Encode_words(data):
	dev = "<s>"
	for sen in data:
		line = sen.split()
		for word in line :
			word = word
			dev = dev + word + " "
	return dev
			
def Linear_Interpolation(data,beta, gamma,count, unique_words, unigram, bigram, trigram):
	prob = 0
	prev1_word = "<s>"
	prev2_word = "<s>"
	data = data.split()
	for word in data:
		p = 0
		biword = prev2_word + " "+ word
		triword = prev1_word + " " + prev2_word + " " + word
		unicount = unigram[word]-beta
		lambda1 = bigram[biword]/float(bigram[biword] + gamma)
		lambda2 = (1-lambda1)*(unicount/float(unicount + gamma))
		lambda3 = 1-lambda1-lambda2
		if lambda1!=0:
			p = p + lambda1*(trigram[triword]/float(bigram[biword]))
		if lambda2!=0 and unicount > 0:
			#print(bigram[biword]/float(unigram[word]))
			p = p + lambda2*(bigram[biword]/float(unicount))	
		if lambda3!=0:
			if word not in unique_words:
				p = p + lambda3*((beta*len(unique_words))/float(count))
			else:
				p = p + lambda3*((unicount)/float(count))
		prob = prob + math.log(p)
		prev1_word = prev2_word
		prev2_word = word
		#print(lambda1, lambda2, lambda3)	
	return prob

def Katz(data,beta,betab,alpha_v,count, unique_words,unigram, bigram, alphasum, Bcount):
	prob = 0
	#prev1_word = "<s>".encode('utf-8')
	prev2_word = "<s>"
	data = data.split()
	for (cnt,word) in enumerate(data):
		p = 0
		biword = prev2_word + " " + word
		unicount = unigram[word] - beta
		if bigram[biword]!=0 and unigram[word]!=0:
			#print("Actual Count",cnt)
			p  = p + ((bigram[biword]-betab)/float(unicount))
		elif unigram[word]!=0 and prev2_word in unique_words and alphasum[prev2_word]!=0:
			#print("Alpha discounted" ,alpha_v[prev2_word], cnt)
			p = p + alpha_v[prev2_word]*(unicount/float(alphasum[prev2_word]- beta*Bcount[prev2_word]))
		else:
			#print("Unigram count",cnt)
			p  = p + (beta*len(unique_words))/float(count)
		prob = prob + math.log(p)
		prev2_word = word
            
	return prob
	
def total_cnt(continuation, unique_words):
    total_cnt = 0
    
    for word in unique_words:
        #print(word, continuation)
        #print(sum(continuation[word].values()))
        total_cnt =total_cnt + len(continuation[word])
    return total_cnt
    
def Kneser_Ney(data,beta,continuation,count,unique_words,unigram, bigram):
	prob = 0
	counthere = 0
	countthere =0
	total_count = total_cnt(continuation, unique_words)
	#prev1_word = "<s>".encode('utf-8')
	prev2_word = "<s>"
	data = data.split()
	#print(len(data))
	for (cnt,word) in enumerate(data):
		if word != "<s>":
			p = 0
		    	biword = prev2_word + " " + word
		    	unicount = unigram[word] - beta
		    	if unigram[word]!=0:
				#print("Actual Count",cnt)
			    	p  = p + (max(0,(bigram[biword]-beta))/float(unicount))
			    	wcnt = len(continuation[word])
			    	pcont = wcnt/float(total_count)
			    	#print("Pcont =",pcont, "unicont = ", unicount)
			    	lambda1 = beta*wcnt/float(unicount)
			    	p = p + lambda1*pcont
			    	#print("P = ",p)
			    	counthere+=1
		    	else:
				#print("Unigram count",cnt)
		        	p  = p + (beta*len(unique_words))/float(count)
			    	countthere +=1
        
        		#print(p,cnt)
        		prob = prob + math.log(p)
        	prev2_word = word
        #print(counthere,countthere)
	return prob
def Count_freq( unicount ):
	freq = Counter()
	for c in list(unicount.values()):
		freq.update([c])
	return freq

def GoodTuring(data,freq,count,unigram):
	prob = 0
	#print(freq[1])
	#print(count)
	data = data.split()
	for word in data:
		#print(word)
		if word != "<s>":
			p = 0
			cnt = unigram[word]
			#print(word , cnt)
			if cnt == 0:
				#print("Count 0")
				p = freq[1]/float(count)
			elif freq[cnt+1]!=0 and freq[cnt]!=0:
				adj_cnt = unigram[word]*freq[cnt+1]/float(freq[cnt])
				#print("Adjusted")
				p = adj_cnt/float(count)
			else:
				#print("Normal")
				p = unigram[word]/float(count)
			prob = prob + math.log(p)
	return prob
    

def cal_perplexity(filename, ext):
          
    pickle_in = open(ext+"unique_wd.pickle","rb")
    unique_words = pickle.load(pickle_in)
    pickle_in.close()
    pickle_in = open(ext+"hyper_dic.pickle","rb")
    hyperparameter = pickle.load(pickle_in)
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
    pickle_in = open(ext+"Bcount.pickle","rb")
    Bcount = pickle.load(pickle_in)
    pickle_in.close()


    with open(filename,"rb") as handle:
        dev_data = pickle.load(handle)

    #dev_data = Encode_words(dev_data)
    #print(dev_data)
    count = word_count(dev_data)
    freq = Count_freq(unigram)
    #print("Words = ",count)
    tr_cnt = sum(unigram.values())
    #print(unigram)
    
    print("GOOD TURING MODEL")
    prob = GoodTuring(dev_data,freq,tr_cnt,unigram)
    perplexity = math.exp(prob/float(-1*count))
    print("Perplexity = ",perplexity)

    print("LINEAR INTERPOLATION")
    prob = Linear_Interpolation(dev_data,hyperparameter["Linear_beta"], hyperparameter["Linear_gamma"],tr_cnt,unique_words,unigram, bigram, trigram)
    perplexity = math.exp(prob/float(-1*count))
    print("Perplexity = ",perplexity)
    
    print("Katz Back-off MODEL")
    alpha_v = alphav(hyperparameter["Katz_betab"], alpha,unique_words)
    prob = Katz(dev_data,hyperparameter["Katz_beta"], hyperparameter["Katz_betab"],alpha_v,tr_cnt,unique_words,unigram, bigram, alphasum, Bcount)
    perplexity = math.exp(prob/float(-1*count))
    print("Perplexity = ",perplexity)
    
    print("Kneser_Ney MODEL",hyperparameter["Kneser_beta"])
    
    prob = Kneser_Ney(dev_data,float(hyperparameter["Kneser_beta"]), continuation,tr_cnt,unique_words,unigram, bigram)
    perplexity = math.exp(prob/float(-1*count))
    print("Perplexity = ",perplexity)
 
print("Test Results")
print("S1: D1train and D1 test")
cal_perplexity("D1test.txt", "D1")  
print("S2: D2train and D2 test")
cal_perplexity("D2test.txt", "D2")
print("S3: D12train and D1 test")
cal_perplexity("D1test.txt", "D12")
print("S4: D12train and D2 test")
cal_perplexity("D2test.txt", "D12")


