# Завантаження словника
def load_dictionary(dictionary_file):
	with open(dictionary_file, 'r', encoding='utf-8') as f:
		dictionary = [word.strip() for word in f.readlines()]
		#print(dictionary[:10])
	return dictionary
words_list = load_dictionary("junyucidian_orfo_sorted_.txt")
# Підрахунок кількості слів за довжиною у словнику
def count_words_by_length(word_dict):
	word_count = {}
	for word in word_dict:
		length = len(word)
		if length in word_count:
			word_count[length] += 1
		else:
			word_count[length] = 1
	return word_count
word_count_by_length = count_words_by_length(words_list)
# Виведення результату
for length, count in sorted(word_count_by_length.items()):# , key=lambda x: x[1], reverse=True
	print(f"Довжина {length}: {count} слів")
#побудова діаграми довжини слів
import numpy as np
import matplotlib.pyplot as plt
# Extract lengths and counts for plotting
lengths = list(word_count_by_length.keys())
counts = list(word_count_by_length.values())
# Plotting
plt.bar(lengths, counts)
plt.xlabel('Довжина слова')
plt.ylabel('Кількість слів')
plt.title('Підрахунок кількості слів за довжиною у словнику')
plt.xticks(np.arange(min(lengths), max(lengths)+1, 1)) 
plt.grid(True)
plt.show()
#підрахунок біграм
def find_repeated_bigrams(words_list):
	bigram_counter = {}
	for word in words_list:
		if len(word) < 2: continue
		for i in range(len(word) - 1):# 2 for threegram
			bigram = word[i:i+2]#Extract the bigram, +3 threegram
			if bigram not in bigram_counter: bigram_counter[bigram] = 0
			bigram_counter[bigram] += 1
	return bigram_counter
# Знаходимо біграми, що повторюються, та їх кількість
repeated_bigrams = find_repeated_bigrams(words_list)
print("Повторюючіся біграми та їх кількість:")
for bigram, count in sorted(repeated_bigrams.items(), key=lambda x: x[1], reverse=True):
	if count >= 25:
		print(f"{bigram}: {count}")
