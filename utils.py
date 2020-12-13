import os
import json
from pathlib import Path


def generate_party_mapping():
    result_folder = Path(__file__).parent / "results"
    filepath = result_folder / "word_occurrence.json"
    with filepath.open() as f:
        content = json.load(f)

    president_name = sorted(content.keys())

    name_party_map = {}
    for i in president_name:
        name_party_map[i] = "D"
        # name_party_map[i[5:]] = "D"

    export_path = result_folder / "name_party.json"
    with export_path.open("w") as f:
        json.dump(name_party_map, f, indent=4)


if __name__ == "__main__":
    generate_party_mapping()
