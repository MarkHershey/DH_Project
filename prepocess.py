import os
import string
from pathlib import Path
from typing import List, Dict
from markkk.logger import logger
from markkk.encoding import is_ascii
from collections import OrderedDict
import nltk
import json
from stopwords import NLTK_STOPWORDS


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
                if is_ascii(w):
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


def get_all_president_word_matrix(master_occurence_map: Dict[str, Dict]):
    names = list(sorted(master_occurence_map.keys()))
    total_word_occurence_map = {}
    for _, v in master_occurence_map.items():
        for word, num in v.items():
            if word in total_word_occurence_map:
                total_word_occurence_map[word] += num
            else:
                total_word_occurence_map[word] = num

    most_frequent_word_list = [
        k
        for k in sorted(
            total_word_occurence_map.keys(),
            key=lambda x: total_word_occurence_map[x],
            reverse=True,
        )
    ]
    csv_data = []
    for word in most_frequent_word_list:
        row_data = [word]
        for president in names:
            if word in master_occurence_map[president]:
                row_data.append(master_occurence_map[president][word])
            else:
                row_data.append(0)
        csv_data.append(row_data)
    names.insert(0, "POTUS")
    csv_data.insert(0, names)

    csv_string_list = []
    for row in csv_data:
        row = [str(i) for i in row]
        csv_string_list.append(", ".join(row))

    export_path = result_folder / "word_occurence.csv"
    with export_path.open("w") as f:
        f.write("\n".join(csv_string_list))
        logger.debug(f"Exported: {export_path}")


def get_word_frequency(master_occurence_map: Dict[str, Dict]):
    names = list(sorted(master_occurence_map.keys()))
    word_frequency_map = {}
    for name in names:
        data = master_occurence_map[name]
        wordcount = sum(data.values())
        freq_data = {}
        for word, count in data.items():
            freq = count / wordcount
            freq_data[word] = freq
        word_frequency_map[name] = freq_data

    export_path = result_folder / "word_frequency.json"
    with export_path.open("w") as f:
        json.dump(word_frequency_map, f, indent=4)
        logger.debug(f"Exported: {export_path}")


def generate_data_for_p1(master_occurence_map: Dict[str, Dict]):
    year_name_key = list(sorted(master_occurence_map.keys()))
    # get the latest
    year_name_key = year_name_key[-2:]

    directed_connections = ["source,target,value"]

    for president in year_name_key:
        data = master_occurence_map.get(president)
        for word, count in data.items():
            record = president[5:] + "," + word + "," + str(count)
            directed_connections.append(record)

    export_path = result_folder / "word_directed_graph.csv"
    with export_path.open("w") as f:
        f.write("\n".join(directed_connections))
        logger.debug(f"Exported: {export_path}")


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
            logger.info(
                f"Number of unique words: {len(word_occurence_map.keys())}")
            # filter stopwords, remove words that once appeared once
            word_occurence_map = {
                k: v
                for k, v in sorted(
                    word_occurence_map.items(), key=lambda x: x[1], reverse=True
                )
                if v > 1 and k not in NLTK_STOPWORDS
            }
            word_occurence_result[filename[:-4]] = word_occurence_map

    # get_all_president_word_matrix(word_occurence_result)
    # generate_data_for_p1(word_occurence_result)
    get_word_frequency(word_occurence_result)

    export_path = result_folder / "word_occurence.json"
    with export_path.open("w") as f:
        json.dump(word_occurence_result, f, indent=4)
