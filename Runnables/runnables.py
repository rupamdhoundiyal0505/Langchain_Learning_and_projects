# The concept of chains 

# Before Langchain had a good chain system, you had to manually pass outputs from
# one component to next, wrtie glue code by yourself. There is no standard way 
# to compose LLM workflows

# -> Format a prompt -> manually call LLM -> manually parse output -> repeat
# -> No way to stream intermidiate steps
# -> No parallel execution no branching no retries


# Runnabels 
# A runnable is anything that has a standard interface - .invoke() .stream() .batch()
# Prompts, LLMs, Parsers, even python fxn are all runnables

# A chain is just multiple runnables connected together using a pipe op

# prompt | llm | parser =  chain


# LCEL : stands for LangChain Expression Language 
# prompt | llm | parser - composable pipeline

from annotated_types import UpperCase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser

# from main import result
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Explain like you are a {field} expert. write at least 25 words"),
        ("user", "Explain {topic}")
    ]
)
prompt = prompt.partial(field = "Python")

llm = ChatOllama(model = "gemma3:270m" ,temperature=0)
chain = prompt | llm | StrOutputParser()

# for chunk in chain.stream({"topic":"recursion"}):
#     print(chunk, end = "", flush=True)


# we can also run multiple inputs in parallel

# results = chain.batch([
#     {"topic" : "recusrion"},
#     {"topic":"hashmap"}
# ])

# print(type(results))

# print(results.content)
# print(results[0], results[1])
# print(results)


# We can append a runnable lambda at the chain like uppercase


chain2 = prompt | llm | StrOutputParser() | RunnableLambda(lambda x: x.upper()+"!!!")
results = chain2.invoke({"topic": "Recursion"})
print(results)