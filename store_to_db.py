from embedder_and_retriver import vector_store
from load_pdf import load_pdf
from split_docs import split_docs


docs = load_pdf()
split_documents = split_docs(docs)

vector_store.add_documents(documents=split_documents)
print("Injection Done")