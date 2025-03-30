from pdfminer.high_level import extract_text
from pathlib import Path
from tqdm import tqdm


pdf_path = "data/pdf/"
txt_path = "data/txt/"

directory = Path(pdf_path)
filenames = [f.name for f in directory.iterdir() if f.suffix == ".pdf"]


def pdf_to_text(pdf_path):
    return extract_text(pdf_path)


for filename in tqdm(filenames):
    with open(txt_path + filename.replace(".pdf", ".txt"), "w") as f:
        f.write(pdf_to_text(pdf_path + filename))

