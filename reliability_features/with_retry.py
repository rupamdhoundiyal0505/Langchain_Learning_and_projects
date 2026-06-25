from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama



# We can also have retry feature it's like if there is an error like limit hit or api not working we can specify to retry so that our production dont break

# It comes up with 3 methods like

llm = ChatOllama(model = "llama3.2:1b", temperature=0)
llm2 = ChatOllama(model = "gemma3:270m", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system" , "You are a coding expert"),
    ("user" ,  "Explain {topic}")
])

primary_chain = prompt | llm | StrOutputParser()
backup_chain = prompt | llm2 | StrOutputParser()


# method 1 : just retry for x number of attempts

reliable_chain = primary_chain.with_retry(
    stop_after_attempt=2,
    wait_exponential_jitter=True
)

# MEethod 2 : Retry on specifc conditions only

reliable_chain2 = primary_chain.with_retry(
    stop_after_attempt=2,
    retry_if_exception_type={TimeoutError}
) 

# Method 3 : merge with fallbacks to make a good system

production_chain = (
    primary_chain
    .with_retry(stop_after_attempt=3)
    .with_fallbacks([backup_chain])
)

results = production_chain.invoke({"topic":"Hashmap"})
print(results)