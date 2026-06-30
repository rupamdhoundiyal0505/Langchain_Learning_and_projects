from langchain_community.document_loaders import (
    TextLoader,
    PyMuPDFLoader,
    WebBaseLoader,
    CSVLoader,
    DirectoryLoader,
    PyPDFLoader
)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module = "langchain_community")
text_load = TextLoader("notes.txt", encoding="utf-8")
docs = text_load.load()

# print(type(docs))
# print(docs)


pdf_load = PyPDFLoader("bin.pdf")
pdf_data = pdf_load.load()

# print(pdf_data.content)

print(len(docs))

print(docs[0].page_content)
print(docs[0].metadata)


print(pdf_data[1].page_content)
print(pdf_data[1].metadata)