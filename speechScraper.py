import requests
from pathlib import Path
from markkk.logger import logger
import base64
from re import compile
from bs4 import BeautifulSoup
from bs4.element import Tag
import logging
from typing import List

logger.setLevel(logging.INFO)


def break_text_into_sentences(text: str) -> List[str]:
    sentences = []
    new_text = ""
    for i in text:
        if i == ".":
            new_text += i
            sentences.append(new_text.strip())
            new_text = ""
        elif i == "\n":
            new_text += " "
        else:
            new_text += i
    return sentences


def extract_info_from_html(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")
    speech_content_div_tag = soup.find("div", class_="field-docs-content")

    paragraphs = []
    for p_tag in speech_content_div_tag.contents:
        if type(p_tag) == Tag:
            _string = p_tag.string
            if _string:
                paragraphs.append(_string.strip())

    full_text = " ".join(paragraphs)
    sentences = break_text_into_sentences(full_text)

    president_name_div_tag = soup.find("div", class_="field-title")
    president_name = None

    for i in president_name_div_tag.contents:
        if type(i) == Tag:
            president_name = i.contents[0].text

    span_tag = soup.find("span", class_="presidential-ordinal-number")
    president_seq = span_tag.text

    speech_year_span_tag = soup.find("span", class_="date-display-single")
    speech_year = speech_year_span_tag.text.strip()
    speech_year = speech_year[-4:]

    logger.info(
        f"{president_seq} President of the United States: {president_name}")

    return speech_year, president_name, sentences


def main():
    with open("links.txt") as f:
        links = f.readlines()

    for link in links:
        page_url = link.strip()
        r = requests.get(page_url)
        if r.status_code == 200:
            logger.info(page_url)
            html_content = r.text
            speech_year, president_name, sentences = extract_info_from_html(
                html_content
            )
            logger.info(speech_year)
            logger.info(president_name)
            export_path = (
                Path("Inaugural_Addresses") /
                f"{speech_year} {president_name}.txt"
            )
            with export_path.open("w") as f:
                f.write("\n".join(sentences))
            logger.info(f"Exported: {export_path}")

        else:
            logger.error(page_url)
            logger.error("Unexpected response with non-200 error code")


if __name__ == "__main__":
    main()
