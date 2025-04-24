from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def load_pdf():
    pdf_path = Path(__file__).parent / "uploads" / "test.pdf"
    loader = PyPDFLoader(file_path=pdf_path)
    docs = loader.load()
    return docs
    # print(docs)

if __name__ == "__main__":
    load_pdf()