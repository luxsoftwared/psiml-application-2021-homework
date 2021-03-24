
from nltk.stem import SnowballStemmer 
from nltk.tokenize import word_tokenize, sent_tokenize
import os
import math
import sys

sys.stdout.reconfigure(encoding='utf-8')
stemmer=SnowballStemmer(language='english')

def binarySearch(array,element):
    bin_start=0
    bin_end=len(array)-1
    mid=(bin_start+bin_end)//2
    while bin_start<=bin_end:
        if element==array[mid][0]:
            break
        if element<array[mid][0]:
            bin_end=mid-1
        else:
            bin_start=mid+1
        mid=(bin_start+bin_end)//2
    else:
        mid=mid+1  
    return mid      #if not found, returns index where element is supposed to be

pathToCorp=input()             
pathToDoc=input()            
array=[]    #array containing elements in format (stem,Term Frequency,Document Frequency)
num_of_docs=0

file=open(pathToDoc,encoding='utf-8')
Text=file.read()
word_tokens=word_tokenize(Text)
sentences=sent_tokenize(Text)
for token in word_tokens:
    if token.isalnum():
        stem=stemmer.stem(token.lower())
        i=binarySearch(array,stem)

        #if stem doesnt exist in array, it is added, otherwise its term freq. is increased
        if i<len(array):
            if array[i][0]==stem :
                array[i][1]+=1
            else:    
                array.insert(i,[stem,1,1])
        else:
            array.append([stem,1,1])

file.close()

for dirpath,dirnames,filenames in os.walk(pathToCorp):
    for filename in filenames:
        num_of_docs+=1
        if os.path.join(dirpath,filename)==pathToDoc:
            continue
        file=open(os.path.join(dirpath,filename),encoding='utf-8')
        tokens=word_tokenize(file.read())
        already_counted=[False]*len(array)  
        for token in tokens:
            if token.isalnum():
                stem=stemmer.stem(token.lower())
                
                i=binarySearch(array,stem)
                
                if i>=len(array) or stem!=array[i][0] or already_counted[i]:
                    continue    
                array[i][2]+=1      #increasing document frequency if stem is encounterede for the first time in this doc, and marking it as already counted
                already_counted[i]=True

        file.close()


for term in array :
    term.append(term[1]*math.log(num_of_docs/term[2],10)) #calculating TF-IDF

result1=[]
visited=[False]*len(array)
for x in range(min(10,len(array))):
    max=-1
    id=-1
    for i in range(len(array)):
        if visited[i] or array[i][3]<=max:
            continue
        max=array[i][3]
        id=i
    visited[id]=True
    result1.append(array[id][0])


result1formated=""
for term in result1:
    result1formated+=term+", "
print(result1formated[:-2])

#SECOND PART
sent_array=[]
n=0
for sentence in sentences:
    words=word_tokenize(sentence)
    important_words_TFIDF=0 
    visited=[False]*len(words)
    for x in range(min(10,len(words))):
        max=-1
        id_in_arr=-1
        id_in_words=-1
        for i in range(len(words)):
            if visited[i] or (not words[i].isalnum()):
                continue

            k=binarySearch(array,stemmer.stem(words[i].lower()))
            
            
            if array[k][3]>max:
                max=array[k][3]
                id_in_arr=k
                id_in_words=i
        important_words_TFIDF+=array[id_in_arr][3]
        visited[id_in_words]=True
    i=0
    while i<len(sent_array) and important_words_TFIDF<=sent_array[i][1]:
        i+=1
    sent_array.insert(i,(sentence,important_words_TFIDF,n))
    n+=1


result2=""
visited=[False]*min(5,len(sent_array))
for x in range(min(5,len(sent_array))):
    minimum=len(sent_array)
    index=0
    for z in range(min(5,len(sent_array))):
        if (not visited[z]) and sent_array[z][2]<minimum:
            minimum=sent_array[z][2]
            index=z
    visited[index]=True
    result2+=sent_array[index][0]+" "

print(result2[:-1])
