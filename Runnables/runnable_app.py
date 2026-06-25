from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableBranch, RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_ollama import ChatOllama



# parallel = RunnableParallel(
#     summary=summary_chain,
#     sentiment=sentiment_chain
# )

# you're defining the keys of the output dictionary.

# from langchain_core.runnables import RunnablePassthrough

# RunnableParallel(
#     context=retriever,
#     question=RunnablePassthrough()
# )
# {
#     "context": ["Doc1", "Doc2"],
#     "question": "What is LangChain?"
# }
llm_classification = ChatOllama(model = "llama3.2:1b", temperature=0)
classification_prompt = ChatPromptTemplate.from_template(
    "Classify user query into ONE word: 'code', 'math','general. Query={query}"
)
classifier_chain = classification_prompt | llm_classification | StrOutputParser()

llm = ChatOllama(model = "llama3.2:1b", temperature=0)

base_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {domain} expert.Print your name everytime you answer just say i am {domain} expert"),
    ("user", "Tell me about {query}")
])
code_prompt = base_prompt.partial(domain = "coding")
math_prompt = base_prompt.partial(domain = "math")
gen_prompt = base_prompt.partial(domain = "general")

code_chain = code_prompt | llm | StrOutputParser()
math_chain = math_prompt | llm | StrOutputParser()
gen_chain = gen_prompt | llm | StrOutputParser()

router = RunnableBranch(
    (lambda x : "code" in x["intent"], code_chain),
    (lambda x : "math" in x["intent"], math_chain),
    gen_chain
)


final_pipeline = (
    RunnableParallel({
        "intent" : classifier_chain,
        "query" : RunnablePassthrough() | RunnableLambda(lambda x : x["query"])
    }) | router
)


# results = final_pipeline.invoke({"query":"Explain pythogores theorem?"})
# print(results)

for chunk in final_pipeline.stream({"query":"Explain Hashmaps"}):
    print(chunk, end="", flush=True)