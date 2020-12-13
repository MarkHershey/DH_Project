import os
import json
from pathlib import Path
from typing import List
from markkk.logger import logger

def part_of_speech():
    result_folder = Path(__file__).parent / "results"
    filepath = result_folder / "tokenised_with_tag.json"

    with filepath.open() as f:
        content = json.load(f)

    president_names = sorted(content.keys())

    part_of_speech_map = {}
    all_tags = []
    for name in president_names:
        part_of_speech_map[name] = {}
        data: List[List[str]] = content[name]
        for i in data:
            word = i[0]
            tag = i[1]

            # NOTE: simplify tags 
            if tag.startswith("NN"):
                tag = "Noun"
            elif tag.startswith("VB"):
                tag = "Verb"
            elif tag.startswith("JJ"):
                tag = "Adj."
            elif tag == "MD":
                tag = "Modal"
            elif tag.startswith("RB"):
                tag = "Adv."
            elif tag.startswith("PRP"):
                tag = "Pronoun"
            else:
                continue

            # get all tags
            if tag not in all_tags:
                all_tags.append(tag)
            
            # count tags
            if tag in part_of_speech_map[name]:
                part_of_speech_map[name][tag] += 1
            else:
                part_of_speech_map[name][tag] = 1
    
    all_tags = sorted(all_tags)
    csv_data = []
    for name in president_names:
        row_data = [name]
        tag_count_map = part_of_speech_map[name]
        for tag in all_tags:
            if tag in tag_count_map:
                row_data.append(str(tag_count_map[tag]))
            else:
                row_data.append("0")

        csv_data.append(",".join(row_data))

    header = ["POTUS"] + all_tags
    csv_data.insert(0, ",".join(header))



    export_path = result_folder / "part_of_speech_count.json"
    with export_path.open("w") as f:
        json.dump(part_of_speech_map, f, indent=4)
    logger.debug(f"Exported: {export_path}")
    export_path = result_folder / "part_of_speech_count.csv"
    with export_path.open("w") as f:
        f.write("\n".join(csv_data))
    logger.debug(f"Exported: {export_path}")


if __name__ == "__main__":
    part_of_speech()
