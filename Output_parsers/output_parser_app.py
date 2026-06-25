from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama


class CodeReview(BaseModel):
    continent : str = Field(description="to which continent user's country belong to")
    nearby_places : str = Field(description="Places to visit")
    cost : str = Field(description="cost of 1 week tour in INR")



parser = PydanticOutputParser(pydantic_object= CodeReview)
# print(parser.get_format_instructions())
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a tour guide \n{format_instructions}"),
    ("user", "I am planning to go to \n {place}")
]).partial(format_instructions = parser.get_format_instructions())


# final_prompt = prompt.invoke({"code":"a=10 b=0 print(a/b)"})
# print(final_prompt)

llm = ChatOllama(model = "qwen3:4b", temperature=1)

chain = prompt | llm  | parser
# results = ""
try:
    results = chain.invoke({
        "place" : "USA"
    })
except Exception as e:
    print(f"Parsing failed: {e}")
# print(results.content)
print(results)
print(type(results))
print(results.nearby_places)
print(results.continent)