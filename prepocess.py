import os
from pathlib import Path
from markkk.logger import logger 

src_folder = Path(__file__).parent / "Inaugural_Addresses"


def prepocess_text(text:str):
    pass


if __name__ == '__main__':
    for filename in os.listdir(src_folder):
        filepath = src_folder / filename
        assert filepath.is_file()
        logger.debug(filepath)
        with filepath.open() as f:
            t = f.read()
            prepocess_text(t)
            break