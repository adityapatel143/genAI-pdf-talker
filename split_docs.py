from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_docs(docs=None):
     # If no documents provided, short-circuit with None
    if docs is None:
        return None

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    return text_splitter.split_documents(docs)

if __name__ == "__main__":
    split_docs()