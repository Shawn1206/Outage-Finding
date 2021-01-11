# this file is for generating word map of certain text dataset, you can use
# the output to extract some feature of your dataset
import json
from collections import defaultdict
from constant import stop_words

word_count = defaultdict(int)
file = open('loca_Isservicedown.json')  # enter your file name
data = json.load(file)
for i in data.values():
    for entry in i:
        words = entry.split(' ')
        for word in words:
            if word.lower() not in stop_words:
                word_clean = ''.join(e for e in word.lower() if e.isalpha())  # get rid of the stop-words
                if word_clean and word_clean not in stop_words:
                    word_count[word_clean] += 1
# sort and print the top 100 frequent words
res = sorted(word_count.items(), key=lambda item: item[1], reverse=True)[:100]
res2 = [e[0] for e in res]
print(res2)
