import os
import string
from pathlib import Path
from typing import List, Dict
from markkk.logger import logger
from collections import OrderedDict
import nltk
import json

STOPWORDS = "the of and to in that a with are as be this it is by or".split()


def removePunctuations(target):
    """
    this function takes in a string, and returns it after removing all
    leading and trailing punctuations
    string.punctuation !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    logic: to find a starting index and ending index to slice the string
    """
    # initialise start and end variable
    start = 0
    end = len(target)
    # find the first non-punctuation char
    for i in range(end):
        if target[i] not in string.punctuation:
            start = i
            break
    # find the last non-punctuation char
    while end >= 1:
        if target[end - 1] not in string.punctuation:
            break
        end -= 1
    # slice the string and return
    return target[start:end]


def get_word_list_from_lines(lines: List[str]) -> List[str]:
    words = []
    for line in lines:
        line = line.strip()
        line_words = line.split()
        for word in line_words:
            w = removePunctuations(word).strip()
            if w not in ("", " ", None):
                words.append(w)
    return words


def get_word_occurence_map(words: List[str]) -> Dict[str, int]:
    occurence_map = dict()
    for word in words:
        word = word.lower()
        if word in occurence_map:
            occurence_map[word] += 1
        else:
            occurence_map[word] = 1
    occurence_map = {
        k: v
        for k, v in sorted(
            occurence_map.items(), key=lambda item: item[1], reverse=True
        )
    }
    return occurence_map


if __name__ == "__main__":
    src_folder = Path(__file__).parent / "Inaugural_Addresses"
    result_folder = Path(__file__).parent / "results"

    word_occurence_result = {}

    for filename in os.listdir(src_folder):
        filepath = src_folder / filename
        assert filepath.is_file()
        logger.debug(filename)
        with filepath.open() as f:
            lines = f.readlines()
            logger.info(f"Number of sentences: {len(lines)}")

            words = get_word_list_from_lines(lines)
            logger.info(f"Number of words: {len(words)}")

            word_occurence_map = get_word_occurence_map(words)
            logger.info(f"Number of unique words: {len(word_occurence_map.keys())}")
            # filter stopwords, remove words that once appeared once
            word_occurence_map = {
                k: v
                for k, v in sorted(
                    word_occurence_map.items(), key=lambda x: x[1], reverse=True
                )
                if v > 10 and k not in STOPWORDS
            }
            word_occurence_result[filename[:-4]] = word_occurence_map


    export_path = result_folder / "word_occurence.json"
    with export_path.open("w") as f:
        json.dump(word_occurence_result,f, indent=4)
