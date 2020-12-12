import os
import json
from pathlib import Path
from typing import Pattern
from markkk.logger import logger

result_folder = Path(__file__).parent / "results"


def get_by_party():
    word_by_party = {}
    occurence_filepath = result_folder / "word_occurence.json"
    with occurence_filepath.open() as f:
        occurence_by_name = json.load(f)

    name_party_filepath = result_folder / "name_party.json"
    with name_party_filepath.open() as f:
        name_party_map = json.load(f)

    # combine into master dict
    for name, data in occurence_by_name.items():
        party = name_party_map[name]
        if party not in ("D", "P"):
            continue
        if party not in word_by_party:
            word_by_party[party] = {}

        for word, count in data.items():
            if word in word_by_party[party]:
                word_by_party[party][word] += count
            else:
                word_by_party[party][word] = 1

    # sort dict
    # TODO

    # write to json
    export_filepath = result_folder / "word_occurence_by_party.json"
    with export_filepath.open("w") as f:
        json.dump(word_by_party, f, indent=4)
    logger.debug(f"Exported: {export_filepath}")


if __name__ == "__main__":
    get_by_party()
