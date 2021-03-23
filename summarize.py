#!/usr/bin/python
import sys
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

import nltk

nltk.download("stopwords")
nltk.download("punkt")
lang_stopwords = []

from nltk.tokenize import sent_tokenize
import networkx as nx
import re


def sentence_stem(sentence, lang):
    """ takes article text and language as inputs, returns a list of stemmed sentences"""
    from nltk.stem.snowball import SnowballStemmer
    if len(lang_stopwords) == 0:
        lang_stopwords = stopwords.words(lang)
    word_arr = [
        SnowballStemmer(lang).stem(word)
        for word in sentence.strip().split()
        if not (word in lang_stopwords)
    ]
    stemmed_sentence = " ".join(word_arr)
    return stemmed_sentence


def tldr_matrix(article, lang):
    """ takes article text and language as inputs, returns a scored list of importance for all the sentences"""
    article = re.sub(r"[^\w\s\.]", " ", article).lower()
    sentences = sent_tokenize(article, language=lang)
    stemmed_sentences = [sentence_stem(sentence, lang) for sentence in sentences]

    bagofwords_matrix = CountVectorizer().fit_transform(stemmed_sentences)
    # normalize with TF-IDF
    bagofwords_matrix = TfidfTransformer().fit_transform(bagofwords_matrix)

    # mirror the matrix onto itself to get the similarity edges between sentences
    similarity_matrix = bagofwords_matrix * bagofwords_matrix.T
    similarity_graph = nx.from_scipy_sparse_matrix(similarity_matrix)

    scores = nx.nx.pagerank_scipy(similarity_graph)
    scored_sentences = [(i, s, scores[i]) for i, s in enumerate(sentences)]

    return sorted(scored_sentences, key=lambda x: x[2])


def summarize(article, lang, num_sentences):
    """ takes article text, language, and number of sentences as inputs, returns summarized article limited to the number of sentences"""
    summary = tldr_matrix(article, lang)[:num_sentences]
    return "\n".join([_[1] for _ in sorted(summary, key=lambda x: x[0])])


if __name__ == "__main__":
    # retrieve command line arguments and store them as variables
    inputdir = sys.argv[1]
    lang = sys.argv[2]
    outfile = sys.argv[3]

    import pyspark
    from nltk.corpus import stopwords

    lang_stopwords = stopwords.words(lang)
    sc = pyspark.SparkContext()
    rdd = sc.wholeTextFiles(inputdir)
    summaries = rdd.map(lambda x: summarize(x[1], lang, 3))
    summaries.saveAsTextFile(outfile)
