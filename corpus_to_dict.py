SYMBOLS=set('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-')
def split_chinese_text(text, dictionary):
	words = []
	i = 0; l = len(text)
	while i < l:
		for j in range(i+14, i, -1):
			if text[i:j] in dictionary:
				words.append(text[i:j])
				i = j
				break
		else:
			words.append(text[i:i+1])
			i += 1
#	return ''.join(w + " " if w.upper() not in SYMBOLS else w for w in words)#	return ' '.join(w for w in words)
#	return ''.join(words[i] if words[i].upper() in SYMBOLS and words[i + 1].upper() in SYMBOLS else words[i] + " " for i in range(len(words) - 1))
	return ''.join(w if w.upper() in SYMBOLS and next_w.upper() in SYMBOLS else w + " " for w, next_w in zip(words, words[1:]))

with open("mil_corpus.txt", 'rt', encoding='utf-8') as f1:
	chinese_text = f1.read()		  
with open("zh_orpho.txt", 'r', encoding='utf-8') as f:
	chinese_dictionary = {word.split('+')[0] for word in f.readlines()}
chinese_words = split_chinese_text(chinese_text, chinese_dictionary)
with open("mil_corpus_s_.txt", 'wt', encoding='utf-8') as f2:
	f2.write(chinese_words)
print("файл успішно записаний")


my_dict = {}
список_слів = chinese_words.split()#перетворює строку у список слів
#with open("mil_corpus_s_.txt", 'rt', encoding='utf-8') as f2:
#	chinese_words = f2.read()
for слово in список_слів:
	my_dict.setdefault(слово, 0)
	my_dict[слово] = my_dict[слово] + 1
sorted_dict = dict(sorted(my_dict.items(), key=lambda x: x[1], reverse=True))
#import json
#with open("mil_corpus_dict.txt", 'w', encoding='utf-8') as json_file:
#	json.dump(sorted_dict, json_file, ensure_ascii=False)

import csv
with open("mil_corpus_dict.txt", mode="w", encoding="utf-8", newline="") as file:
	writer = csv.writer(file, delimiter='\t')
	writer.writerow(["слово", "частота"])
	for a, b in sorted_dict.items():
		writer.writerow([a, b])
