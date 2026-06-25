from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableBranch
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate



llm = ChatOllama(model = "gemma3:270m",  temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system","You are a {field} expert also in every answer you mention your name as {field}addict"),
    ("user","explain {topic}")
])

python_chain = prompt.partial(field = "Python ")  | llm | StrOutputParser()
java_chain = prompt.partial(field = "java")  | llm | StrOutputParser()
general_chain = prompt.partial(fiele = "Programmer")  | llm | StrOutputParser()
branch = RunnableBranch(
    (lambda x : "python" in x["topic"].lower(), python_chain),
    (lambda x : "java" in x["topic"].lower(),java_chain),
    general_chain
)


result =  branch.invoke({"topic" : "Explain java loops"})
print(result)


