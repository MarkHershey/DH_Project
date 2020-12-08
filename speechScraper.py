import requests
from pathlib import Path
from markkk.logger import logger
import base64
from re import compile
from bs4 import BeautifulSoup
from bs4.element import Tag
import logging

logger.setLevel(logging.INFO)

def extract_info_from_html(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")
    speech_content_div_tag = soup.find("div", class_="field-docs-content")
    # print(type(speech_content_div_tag))
    paragraphs = []
    for p_tag in speech_content_div_tag.contents:
        if type(p_tag) == Tag:
            _string = p_tag.string
            if _string:
                paragraphs.append(_string.strip())

    # print(paragraphs)

    president_name_div_tag = soup.find("div", class_="field-title")
    president_name = None

    for i in president_name_div_tag.contents:
        if type(i) == Tag:
            president_name = (i.contents[0].text)

    span_tag = soup.find("span", class_="presidential-ordinal-number")
    president_seq = span_tag.text

    term_year_span_tag = soup.find("span", class_="dates")
    term_year = term_year_span_tag.text.strip()
    term_year_start = term_year[:4]


    logger.info(f"{president_seq} President of the United States: {president_name}")

    return term_year_start, president_name, paragraphs


def main():
    base_url = "https://www.presidency.ucsb.edu/documents/inaugural-address-"

    for i in range(53):
        page_url = base_url + str(i)
        r = requests.get(page_url)
        if r.status_code == 200:
            logger.info(i)
            html_content = r.text
            term_year_start, president_name, paragraphs = extract_info_from_html(html_content)
            export_path = Path("Inaugural_Addresses") / f"{term_year_start} {president_name}.txt"
            with export_path.open("w") as f:
                f.write("\n".join(paragraphs))
            logger.info(f"Exported: {export_path}")

        else:
            logger.error(i)
            logger.error("Unexpected response with non-200 error code")

if __name__ == '__main__':
    main()
