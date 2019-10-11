import nltk
from nltk.util import ngrams
from collections import Counter

with open('nlp_input.txt', 'r') as file:
    text = file.read()

# wtokens = nltk.word_tokenize(text)
# print(wtokens)

lemmatizer = nltk.stem.WordNetLemmatizer()

# print(lem_words)
lines = text.split("\n")
words = ' '.join([word for word in lines if word != ""])
wtokens = nltk.word_tokenize(words)
#reference https://machinelearningmastery.com/clean-text-machine-learning-python/
#remove punctuation
wtokens_clean = [word for word in wtokens if word.isalpha()]

lem_words = []

for x in range(len(wtokens_clean)):
    lem_words.append(lemmatizer.lemmatize(wtokens_clean[x], 'v'))

stokens = nltk.sent_tokenize(words)
stoken_list = list(stokens)
#print(stoken_list)

#find the trigrams
trigrams = ngrams(wtokens_clean, 3)

# find frequency of trigrams
trigram_freq = Counter(trigrams)
print("\n")
# print(trigram_freq)
# Print top 10 frequent trigrams
top_10 = trigram_freq.most_common(10)
# print(trigram_freq.most_common(10))

common_phrases = []

for k, v in top_10:
    if k != "":
        print(" ".join(k), v)
        common_phrases.append(" ".join(k))
# print(common_phrases)

common_list = []
for x in stoken_list:
    for y in common_phrases:
        if y in x:
            if x not in common_list:
                common_list.append(x)
#                print(x)

#concatenate the results
print("\n The concatenated list of sentences with most frequent trigrams")
print("********************************************************************")
print(" ".join(common_list))
# common_sent = [sum(y in x for y in common_phrases) for x in stoken_list]
# print(common_sent)