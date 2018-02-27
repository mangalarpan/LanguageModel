#!/usr/bin/python3          
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re
import glob
import errno
import os
import codecs
import numpy as np
import pickle
import sys

reload(sys)
sys.setdefaultencoding('latin-1')

def create_txt(files):
    data= []
    data_blocks = []
    for f in files:
#        with codecs.open(f, 'r','cp1251') as f1:
        with open(f, 'r') as f1:
#            block = read.f1().split("\n\n")
            block = f1.read().split("\n\n")
            for line in block:
                data.append(line)
                
    #print(len(data))          
    for (count,para) in enumerate(data):
        data[count] = re.sub("\\n"," ",para)
    #print(data[3])
    for (count,para) in enumerate(data):
        data[count]= nltk.sent_tokenize(para)
    #print(data[3])
    #print(len(data))
    #punct = [',','.','!','?',';',':','}','{','[',']' ]

    for para in data:
        for line in para:
            tokenized_text = nltk.word_tokenize(line)
            string  = "<s> <s> "
            for word in tokenized_text:
                #if word not in punct:
                word = word.split("/")[0]
                string = string + word + " "
                    
            string = string + "</s> "
            data_blocks.append(string)

    #print(data_blocks[3])
    #print(len(data_blocks))
    return data_blocks

def partition(data_blocks):
    num = np.random.permutation(len(data_blocks))
    data_shuffled = []
    for i in num:
        data_shuffled.append(data_blocks[i])
    i1 = int(len(data_shuffled)*0.8)
    i2 = int(len(data_shuffled)*0.9)
    train_data = data_shuffled[: i1]  
    dev_data = data_shuffled[i1:i2]
    test_data = data_shuffled[i2:]
    
    train = ""
    for i in range(len(train_data)):
        train = train + train_data[i]
    #print(train) 
    dev = ""
    for i in range(len(dev_data)):
        dev = dev + dev_data[i]
    test = ""
    for i in range(len(test_data)):
        test = test + test_data[i]
    return train, dev, test
    
#path = "/run/media/clabuser/Arpan"
#os.chdir(path)
    
all_files = os.listdir("gutenberg")
all_files = ["gutenberg/" + s for s in all_files]
all_files.remove("gutenberg/README")
all_files2 = os.listdir("brown")
all_files2 = ["brown/" + s for s in all_files2]
all_files2.remove("brown/README")
all_files2.remove("brown/cats.txt")
all_files2.remove("brown/CONTENTS")

data_blocks = create_txt(all_files2)
D1_train,D1_dev,D1_test = partition(data_blocks)
data_blocks = create_txt(all_files)
D2_train,D2_dev,D2_test = partition(data_blocks)
data_blocks = create_txt(all_files+all_files2)
D12_train,D12_dev,D12_test = partition(data_blocks)



with open("D1train.txt","wb") as handle:
    pickle.dump(D1_train, handle)
with open("D2train.txt","wb") as handle:
    pickle.dump(D2_train, handle)
with open("D12train.txt","wb") as handle:
    pickle.dump(D12_train, handle)
   
with open("D1dev.txt","wb") as handle:
    pickle.dump(D1_dev, handle)
with open("D2dev.txt","wb") as handle:
    pickle.dump(D2_dev, handle)
with open("D12dev.txt","wb") as handle:
    pickle.dump(D12_dev, handle)
    
with open("D1test.txt","wb") as handle:
    pickle.dump(D1_test, handle)
with open("D2test.txt","wb") as handle:
    pickle.dump(D2_test, handle)
with open("D12test.txt","wb") as handle:
    pickle.dump(D12_test, handle)
