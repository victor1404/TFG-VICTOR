import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from pymongo_get_database import get_database


nltk.download('stopwords')
nltk.download('punkt')

import string
punctuations = string.punctuation

def create_freq_dict(text_string):
    #stopWords = set(stopwords.words("english"))
    stopWords = set(stopwords.words("spanish"))
    words = word_tokenize(text_string.lower())
    ps = PorterStemmer()
    # remove punctuations
    word_frequencies = dict()
    for word in words:
        word = ps.stem(word)
        if ((word in stopWords) or (word in punctuations)):
            continue
        if word in word_frequencies:
            word_frequencies[word] += 1
        else:
            word_frequencies[word] = 1

    return word_frequencies


def score_sentences(sentences, word_frequencies):
    sentence_scores = dict()

    for sentence in sentences:
        word_count = (len(word_tokenize(sentence)))
        word_count_except_sw = 0
        for word in word_frequencies:
            if word in sentence.lower():
                word_count_except_sw += 1
                #if sentence[:10] in sentence_scores:
                if sentence in sentence_scores:
                    #sentence_scores[sentence[:10]] += word_frequencies[word]
                    sentence_scores[sentence] += word_frequencies[word]
                else:
                    #sentence_scores[sentence[:10]] = word_frequencies[word]
                    sentence_scores[sentence] = word_frequencies[word]

        #if sentence[:10] in sentence_scores:
        if sentence in sentence_scores:
            # higher no. of words in a sentence should not make its score higher
            #sentence_scores[sentence[:10]] = sentence_scores[sentence[:10]] / word_count_except_sw  
            sentence_scores[sentence] = sentence_scores[sentence] / word_count_except_sw

    return sentence_scores


def find_average_score(sentence_scores):
    sumValues = 0
    for sentence in sentence_scores:
        sumValues += sentence_scores[sentence]

    # Average value of a sentence from original text
    average = (sumValues / len(sentence_scores))

    return average


def generate_summary(sentences, sentence_scores, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        # if sentence[:10] in sentence_scores and sentence_scores[sentence[:10]] >= (threshold):
        if sentence in sentence_scores and sentence_scores[sentence] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary


def run_summarization(text, threshold=1.3):

    word_frequencies = create_freq_dict(text)
    sentences = sent_tokenize(text)
    sentence_scores = score_sentences(sentences, word_frequencies)
    sentence_avg_score = find_average_score(sentence_scores)
    summary = generate_summary(sentences, sentence_scores, threshold * sentence_avg_score)

    return summary


dbname = get_database()

collection_name = dbname["ProcesosParticipativos"]
item_details = collection_name.find()

for item in item_details:
    if item["_id"] == "avingudamadrid":
        comentarios = item["encuentros"][0]["comentarios"]
        

text = ''.join(comentarios)
threshold = 1.2
summary = run_summarization(text, threshold)
while summary == "":
    threshold -= 0.1
    summary = run_summarization(text, threshold)
print(summary)