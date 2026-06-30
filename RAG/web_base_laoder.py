from langchain_community.document_loaders import WebBaseLoader, CSVLoader


loader = WebBaseLoader("https://reference.langchain.com/python/langchain-community/document_loaders")


docs = loader.load()

print(len(docs))
print(type(docs))

print(docs[0].metadata)


csv_load = CSVLoader(file_path="test.csv",
                    source_column= "id")

docs_csv  =  csv_load.load()

print(type(docs_csv[1].page_content))


# a CSV with 40 columns produces page_content like:
# "col1: val\ncol2: val\ncol3: val\n... col40: val"
# every row = ~500 tokens just from column names

# SOLUTION

# import pandas as pd
# df = pd.read_csv("big_data.csv")[["name","email","plan"]]
# df.to_csv("filtered.csv")
# docs_csv = csv_load()

#df.fillna("").to_csv("clean.csv", index=False)