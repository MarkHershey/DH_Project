import os
import json
from pathlib import Path
from textwrap import indent

# internal
from get_docs import get_all_documents
from graph import stack_bar_chart

# 3rd party
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from markkk.logger import logger

result_folder = Path(__file__).parent / "results"


def generate_word_label():
    names, documents = get_all_documents()
    assert len(names) == len(documents)

    tokenised_with_tag = {}

    for i in range(len(names)):
        name = names[i]
        doc = documents[i]

        # NLTK
        tokenizer = RegexpTokenizer(r'\w+')
        text = tokenizer.tokenize(doc)
        token_tag_list = nltk.pos_tag(text)
        tokenised_with_tag[name] = token_tag_list

    # export
    export_path = result_folder / "tokenised_with_tag.json"
    with export_path.open("w") as f:
        json.dump(tokenised_with_tag, f)
    logger.debug(f"Exported: {export_path}")

    return


def get_stacked_chart_data():
    filepath = result_folder / "tokenised_with_tag.json"
    with filepath.open() as f:
        content = json.load(f)

    master_dict = {}
    for name, token_tag_list in content.items():
        master_dict[name] = {}
        for token_tag in token_tag_list:
            token = token_tag[0]
            tag = token_tag[1]

            if tag in master_dict[name]:
                master_dict[name][tag] += 1
            else:
                master_dict[name][tag] = 1

    fixed_tag_seq = []
    for name, data in master_dict.items():
        for tag in data.keys():
            if tag not in fixed_tag_seq:
                fixed_tag_seq.append(tag)

    fixed_tag_seq = sorted(fixed_tag_seq)

    print(fixed_tag_seq)
    csv_datalist = []
    for name, data in master_dict.items():
        csv_row = [name]
        for tag in fixed_tag_seq:
            if tag in data:
                csv_row.append(str(data[tag]))
            else:
                csv_row.append("0")
        csv_datalist.append(",".join(csv_row))

    fixed_tag_seq.insert(0, "Presidents")
    csv_datalist.insert(0, ",".join(fixed_tag_seq))

    csv_data = "\n".join(csv_datalist)

    # export
    export_path = result_folder / "word_stack_chart.csv"
    with export_path.open("w") as f:
        f.write(csv_data)
    logger.debug(f"Exported: {export_path}")


def get_stacked_chart_data2():
    filepath = result_folder / "tokenised_with_tag.json"
    with filepath.open() as f:
        content = json.load(f)

    master_dict = {}
    for name, token_tag_list in content.items():
        master_dict[name] = {}
        for token_tag in token_tag_list:
            token = token_tag[0]
            tag = token_tag[1]

            if tag in master_dict[name]:
                master_dict[name][tag] += 1
            else:
                master_dict[name][tag] = 1

    fixed_tag_seq = []
    for name, data in master_dict.items():
        for tag in data.keys():
            if tag not in fixed_tag_seq:
                fixed_tag_seq.append(tag)

    fixed_tag_seq = sorted(fixed_tag_seq)[:8]

    print(fixed_tag_seq)
    csv_datalist = {}
    for name, data in master_dict.items():
        csv_row = []
        for tag in fixed_tag_seq:
            if tag in data:
                csv_row.append((data[tag]))
            else:
                csv_row.append(0)
        csv_datalist[name] = csv_row

    stack_bar_chart(csv_datalist, fixed_tag_seq)


if __name__ == "__main__":
    generate_word_label()
    # get_stacked_chart_data()
    # get_stacked_chart_data2()
