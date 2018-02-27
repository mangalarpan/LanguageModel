import pickle
import math
from collections import Counter
import sys

reload(sys)
sys.setdefaultencoding('latin-1')

def create_dic(filename,ext):
    with open(filename,"rb") as handle:
        train = pickle.load(handle)
    #print(len(train))
    #print(train)
    unique_words = [] #list of words in vocabulary
    #train = ""  #create a complete one sentence of train data
    data = train.split() # seprate out words
    unigram = Counter(data)
    print(len(data))
    #train = "<s> "
    """
    for (count,sen) in enumerate(train_data):
	    line = sen.split()
	    for (cnt,word) in enumerate(line) :
		    word = word
		    train = train + word + " "
		    unigram.update([word])
    """
    print("Count of words = " , sum(unigram.values()))       
    unique_words = set(unigram.elements())
    print(len(unique_words))            
    print(unigram.most_common(10)) 

    alpha = dict((name,Counter()) for name in unique_words)
    continuation = dict((name,[]) for name in unique_words)
    alpha_sum = dict((name,0) for name in unique_words)
    Av = dict((name,[]) for name in unique_words)
    Bcount = dict((name,0) for name in unique_words)
    
    bigram = Counter()
    trigram = Counter()
    prev1_word = "<s>"
    prev2_word = "<s>"
    #for word in data:
      #  print(word)
    for word in data:
	    if word != "<s>":
		    alpha[prev2_word].update([word])
		    #print(word)
		    continuation[word].append(prev2_word)
		    #alpha_sum[prev2_word] = alpha_sum[prev2_word] + unigram[word]
		    Av[prev2_word].append(word)
		    biword = prev2_word +" " +word
		    triword = prev1_word + " "+ prev2_word + " "+word
		    bigram.update([biword])
		    trigram.update([triword])
            
	    prev1_word = prev2_word
	    prev2_word = word
	
    unigram_count = sum(unigram.values())  
    length = len(unique_words)
    for word in unique_words:
        Aword = set(Av[word])
        suma = 0
        for elt in Aword:
            suma = suma + unigram[elt]
            
        alpha_sum[word] = unigram_count - suma
        Bcount[word] = length - len(Aword)
    
    print(unigram['<s>'])
    print(bigram.most_common(10)) 
    print(trigram.most_common(10)) 
    for word in unique_words:
        continuation[word] = set(continuation[word])
        
    #store unique words
    pickle_out = open(ext+"unique_wd.pickle","wb")
    pickle.dump(unique_words, pickle_out)
    pickle_out.close()
    #store Bcount
    pickle_out = open(ext+"Bcount.pickle","wb")
    pickle.dump(Bcount, pickle_out)
    pickle_out.close()
    #store unigram_dic
    pickle_out = open(ext + "uni_dic.pickle","wb")
    pickle.dump(unigram, pickle_out)
    pickle_out.close()
    #store bigram_dic
    pickle_out = open(ext+"bi_dic.pickle","wb")
    pickle.dump(bigram, pickle_out)
    pickle_out.close()
    #store trigram_dic
    pickle_out = open(ext+"tri_dic.pickle","wb")
    pickle.dump(trigram, pickle_out)
    pickle_out.close()
    #store alpha_dic
    pickle_out = open(ext+"alpha_dic.pickle","wb")
    pickle.dump(alpha, pickle_out)
    pickle_out.close()
    #store alpha_dic
    pickle_out = open(ext+"alphasum_dic.pickle","wb")
    pickle.dump(alpha_sum, pickle_out)
    pickle_out.close()
    #store cont_dic
    pickle_out = open(ext+"continuation_dic.pickle","wb")
    pickle.dump(continuation, pickle_out)
    pickle_out.close()
    
    
create_dic("D1train.txt","D1")
create_dic("D2train.txt","D2")
create_dic("D12train.txt","D12")
#create_dic("D12train.txt","D12")
