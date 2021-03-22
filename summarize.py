from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import networkx as nx
import re


def sentence_stem(sentence, lang):
    """ takes article text and language as inputs, returns a list of stemmed sentences"""
    word_arr = [
        SnowballStemmer(lang).stem(word)
        for word in sentence.strip().split()
        if not (word in stopwords.words(lang))
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
