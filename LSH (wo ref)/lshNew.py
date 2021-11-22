from random import shuffle
import pandas as pd
import time
import os, psutil
import sys
sys.path.insert(0, 'tf-idf')
import data_cleaning
from data_processor import load_dataset
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#data500 = pd.read_csv('data/mcf_data_500.csv')
#data1000 = pd.read_csv('data/mcf_data_1000.csv')
#data2000 = pd.read_csv('data/mcf_data_2000.csv')
#data3000 = pd.read_csv('data/mcf_data_3000.csv')
#data4000 = pd.read_csv('data/mcf_data_4000.csv')
#data5000 = pd.read_csv('data/mcf_data_5000.csv')
#data10000 = pd.read_csv('data/mcf_data_10000.csv')
DATA_SOURCE = [
  'data/mcf_data_500.csv',
  'data/mcf_data_1000.csv',
  'data/mcf_data_2000.csv',
  'data/mcf_data_3000.csv',
  'data/mcf_data_4000.csv',
  'data/mcf_data_5000.csv',
  'data/mcf_data_10000.csv'
]
DELIMITER = ','

query = 'java javascript react'

#Remove text for all special characters
def cleantext(text):
    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return ''.join(filter(whitelist.__contains__, text))

def shingle(text: str, k: int):
    text = cleantext(text)
    shingle_set = []
    for i in range(len(text) - k+1):
        shingle_set.append(text[i:i+k])
    return set(shingle_set)

def create_hash_func(size: int):
    # function for creating the hash vector/function
    hash_ex = list(range(1, len(vocab)+1))
    shuffle(hash_ex)
    return hash_ex

def build_minhash_func(vocab_size: int, nbits: int):
    # function for building multiple minhash vectors
    hashes = []
    for _ in range(nbits):
        hashes.append(create_hash_func(vocab_size))
    return hashes

def create_hash(vector: list):
    # use this function for creating our signatures (eg the matching)
    signature = []
    for func in minhash_func:
        for i in range(1, len(vocab)+1):
            idx = func.index(i)
            signature_val = vector[idx]
            if signature_val == 1:
                signature.append(i)
                break
    return signature

def jaccard(a: set, b: set):
    return len(a.intersection(b)) / len(a.union(b))

def split_vector(signature, b):
    assert len(signature) % b == 0
    r = int(len(signature) / b)
    # code splitting signature in b parts
    subvecs = []
    for i in range(0, len(signature), r):
        subvecs.append(signature[i : i+r])
    return subvecs

def euclidean_distance(x,y,r=2.0):
    try:
        
        return sum(((x[i] - y[i]) ** r) for i in range(len(x))) ** (1.0/r)
    
    except (ValueError,ZeroDivisionError):
        print('Please, enter only even values for "r > 0".')
    except IndexError:
        print('Please, the sets must have the same size.')

def cosine_distance(x,y):
    prodAB = sum([x[i]*y[i] for i in range(len(x))])
    zeros = [0 for i in range(len(x))]
    A = euclidean_distance(x,zeros)
    B = euclidean_distance(y,zeros)
    return prodAB / (A*B)

results = pd.DataFrame({
    's': [],
    'P': [],
    'r,b': []
})

def probability(s, r, b):
    # s: similarity
    # r: rows (per band)
    # b: number of bands
    return 1 - (1 - s**r)**b

#Part 1: Comment part 1 or part 2 out and run them one at a time
#Graph component showing the effects of b and r on probability of returning a candidate pair
# for s in np.arange(0.01, 1, 0.01):
#     total = 100
#     for b in [100, 50, 25, 20, 10, 5, 4, 2, 1]:
#         r = int(total/b)
#         P = probability(s, r, b)
#         results = results.append({
#             's': s,
#             'P': P,
#             'r,b': f"{r},{b}"
#         }, ignore_index=True)
# sns.lineplot(data=results, x='s', y='P', hue='r,b')
# plt.xlabel("Similarity")
# plt.ylabel("Probability of sharing bucket")
# plt.show()

# Part 2: Comment out either part 1 or part 2 and run them one at a time
# For getting the similarity, time taken and space taken
for DATA_FILES in DATA_SOURCE:
    df = load_dataset(DATA_FILES, DELIMITER)
    cleaned_documents = data_cleaning.DocumentsCleaner().call(df, "description")
    cleaned_documents = cleaned_documents[["uuid",'description_cleaned']]
    
    #change data and k to run different tests
    start_time = time.time()
    k=2
    similarity_list = []
    for lines in cleaned_documents["description_cleaned"]:
        #preparing the shingles
        newquery = shingle(query,k)
        newlines = shingle(lines,k)
        vocab = list(newquery.union(newlines))

        #preparing one hot
        query_1hot = [1 if x in newquery else 0 for x in vocab]
        line_1hot = [1 if x in newlines else 0 for x in vocab]

        minhash_func = build_minhash_func(len(vocab), 20)

        query_sig = create_hash(query_1hot)
        line_sig = create_hash(line_1hot)
        similarity = cosine_distance(query_sig,line_sig)
        similarity_list.append(similarity)

        band_query = split_vector(query_sig, 10)
        band_line = split_vector(line_sig, 10)

    print("New File")
    oldfilesize = df.memory_usage(deep=True).sum()
    newfilesize = cleaned_documents.memory_usage(deep=True).sum()
    print("Memory taken --- %s B ---" % str(df.memory_usage(deep=True).sum()-cleaned_documents.memory_usage(deep=True).sum()))
    print("Time taken --- %s seconds ---" % (time.time() - start_time))
    cleaned_documents["similarity"] = similarity_list
    print(cleaned_documents)