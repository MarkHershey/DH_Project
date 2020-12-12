import os
import string
from pathlib import Path
from typing import List, Dict
from markkk.logger import logger
from collections import OrderedDict
import nltk
import json
from pprint import pprint
from get_docs import *
from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities
import gensim
from stopwords import NLTK_STOPWORDS

STOPWORDS = "the of and to in that a with are as be this it is by or".split()

# NOTE: https://radimrehurek.com/gensim/auto_examples/core/run_similarity_queries.html


def main():
    doc_names, documents = get_all_documents()

    # remove common words and tokenize
    texts = [
        [word for word in gensim.utils.simple_preprocess(
            doc) if word not in NLTK_STOPWORDS]
        for doc in documents
    ]

    # remove words that appear only once
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=30)

    # get trump document
    doc = get_trump_full_text()
    # Convert document into the bag-of-words (BoW) format = list of (token_id, token_count) tuples.
    vec_bow = dictionary.doc2bow(gensim.utils.simple_preprocess(doc))

    # convert the query to LSI space
    vec_lsi = lsi[vec_bow]

    # transform corpus to LSI space and index it
    index = similarities.MatrixSimilarity(lsi[corpus])

    # Index persistency
    index.save("tmp.index")
    index = similarities.MatrixSimilarity.load("tmp.index")

    # perform a similarity query against the corpus
    sims = index[vec_lsi]  # numpy.ndarray

    # print (document_number, document_similarity) 2-tuples
    # print(list(enumerate(sims)))

    sims = sorted(enumerate(sims), key=lambda item: item[1], reverse=True)

    logger.debug("Most similar document on top:")
    for doc_position, doc_score in sims:
        print(
            f"Similarity: {round(float(doc_score), 3)} | {doc_names[doc_position]}")
    for doc_position, doc_score in sims:
        print(float(doc_score))
    for doc_position, doc_score in sims:
        print(doc_names[doc_position])

    with open("results/name_party.json") as f:
        name_party_map = json.load(f)

    for doc_position, doc_score in sims:
        print(name_party_map[doc_names[doc_position]])


if __name__ == "__main__":
    main()
