import json
from collections import defaultdict
from constant import stop_words

word_count = defaultdict(int)
file = open('loca_Isservicedown.json')
data = json.load(file)
for i in data.values():
    for entry in i:
        words = entry.split(' ')
        for word in words:
            if word.lower() not in stop_words:
                word_clean = ''.join(e for e in word.lower() if e.isalpha())
                if word_clean and word_clean not in stop_words:
                    word_count[word_clean] += 1
res = sorted(word_count.items(), key=lambda item: item[1], reverse=True)[:100]
res2 = [e[0] for e in res]
print(res2)
