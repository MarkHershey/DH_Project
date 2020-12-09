import gensim
import os
import string
from pathlib import Path
from typing import List, Dict
from markkk.logger import logger
from collections import OrderedDict
import nltk
import json


def get_all_documents() -> List[str]:
    src_folder = Path(__file__).parent / "Inaugural_Addresses"

    docs = []
    doc_names = []

    for filename in sorted(os.listdir(src_folder)):
        filepath = src_folder / filename
        assert filepath.is_file()
        logger.debug(filename)
        with filepath.open() as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            doc = " ".join(lines)
            doc_names.append(filename[:-4])
            docs.append(doc)

    return doc_names, docs


def get_trump_full_text() -> str:
    src_folder = Path(__file__).parent / "Inaugural_Addresses"
    trump_filepath = src_folder / "2017 Donald J. Trump.txt"
    assert trump_filepath.is_file()
    with trump_filepath.open() as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        doc = " ".join(lines)
        return doc


if __name__ == "__main__":
    get_all_documents()
