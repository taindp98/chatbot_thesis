import csv
import string
from pyvi import ViTokenizer
#1 Lay tung dong file csv
with open("//raw_080820.csv", "r") as ins:
    array = [i.strip() for i in ins]
    #for line in ins:
    #    array.append(line)
doc=array[278]
print(type(doc))
#2 Clean & lower
def clean_document(doc):
    doc = ViTokenizer.tokenize(doc) #Pyvi Vitokenizer library
    doc = doc.lower() #Lower
    tokens = doc.split() #Split in_to words
    table = str.maketrans('', '', string.punctuation.replace("_", "")) #Remove all punctuation
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word]
    return tokens

print(clean_document(doc))

