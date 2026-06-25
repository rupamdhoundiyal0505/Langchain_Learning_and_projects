from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableBranch
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model = "llama3.2:1b", temperature=0)
llm2 = ChatOllama(model = "gemma3:270m", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system" , "You are a coding expert"),
    ("user" ,  "Explain {topic}")
])

primary_chain = prompt | llm | StrOutputParser()
backup_chain = prompt | llm2 | StrOutputParser()

reliable_chain = primary_chain.with_fallbacks([
    backup_chain
])


results = reliable_chain.invoke(
    {"topic" : "recursion"}
)


print(results)
