from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field

class CustomerSupport(BaseModel):
    intent : str = Field(description="billing, technical, or general")
    priority : str = Field(description="determine priority of the query from low medium high")
    response : str = Field(description="Your output solution")

class CustomerSupportOutput(BaseModel):
    intent:       str
    priority:     str
    response:     str
    suggested_kb: str 

parser = PydanticOutputParser(pydantic_object=CustomerSupport)

classification_prompt = PromptTemplate.from_template(
    "Classify this query into EXACTLY one word — billing, technical, or general.\n"
    "Reply with just the word, nothing else.\n"
    "Query: {query}"
)

priority_prompt = PromptTemplate.from_template(
    "Classify this query's priority as EXACTLY one word — low, medium, or high.\n"
    "Reply with just the word, nothing else.\n"
    "Query: {query}"
)

kb_prompt = PromptTemplate.from_template(
    "Suggest ONE relevant knowledge base article title for this support query.\n"
    "Reply with just the article title, nothing else.\n"
    "Query: {query}"
)

# prompt_to_specialist = ChatPromptTemplate.from_messages([
#     ("system" , "You are a {intent} expert and this query has priority{priority} and the Knowledge Base used is {knowledge_base}.Use this format to give response {format}"),
#     ("user" , "Help me solve following query {query}.")

# ]).partial(format = parser.get_format_instructions())

billing_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a billing specialist.
You ONLY handle payment issues, refunds, invoices, and subscription changes.
If query is not billing related, say so.
{format}"""),
    ("user", "Priority: {priority}\nContext: {knowledge_base}\nQuery: {query}")
]).partial(format=parser.get_format_instructions())

technical_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior technical support engineer.
You ONLY handle bugs, errors, crashes, and integration issues.
Always ask for error logs if not provided.
{format}"""),
    ("user", "Priority: {priority}\nContext: {knowledge_base}\nQuery: {query}")
]).partial(format=parser.get_format_instructions())


general_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly customer support agent.
Handle general queries, onboarding questions, and anything not billing or technical.
{format}"""),
    ("user", "Priority: {priority}\nContext: {knowledge_base}\nQuery: {query}")
]).partial(format=parser.get_format_instructions())

llm_single = ChatOllama(model = "llama3.2:1b", temperature=0)
llm_billing = ChatOllama(model = "llama3.2:1b", temperature=0)
llm_technical = ChatOllama(model = "llama3.2:1b", temperature=0)
llm_gen = ChatOllama(model = "gemma3:270m" , temperature=0)

# single_prompt_chain = classification_prompt | llm_gen | StrOutputParser()
billing_chain = billing_prompt | llm_billing | parser
technical_chain = technical_prompt | llm_technical | parser
gen_chain = general_prompt | llm_gen | parser


router = RunnableBranch(
    (lambda x : 'billing' in x["intent"].lower(), billing_chain),
    (lambda x : 'technical' in x["intent"].lower(), technical_chain),
    gen_chain
)
final_chain = (
    RunnableParallel(
        {
            "intent" : classification_prompt | llm_single | StrOutputParser(),
            "priority" : priority_prompt | llm_single | StrOutputParser(),
            "knowledge_base" : kb_prompt | llm_single | StrOutputParser(),
            "query" : RunnableLambda(lambda x : x["query"]),

        }
        
    ) | 


    RunnableParallel({
        "parsed"  : router,
        "knowledge" : RunnableLambda(lambda x : x["knowledge_base"])
    }) | 


    # )|
    RunnableLambda(lambda x : CustomerSupportOutput(
        priority= x["parsed"].priority,
        response= x["parsed"].response,
        suggested_kb= x["knowledge"],
        intent = x["parsed"].intent,))

)

results = final_chain.invoke({"query" : "i want refund for id 20001"})

print(results)



