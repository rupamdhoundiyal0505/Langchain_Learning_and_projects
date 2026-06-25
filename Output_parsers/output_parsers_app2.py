from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama


class CodeReview(BaseModel):
    issues : str = Field(description="list of problems found in the user's code")
    severity : str = Field(description="Overall severity low, medium, high")
    fixed_code : str = Field(description="the corrected version of user's code")



parser = PydanticOutputParser(pydantic_object= CodeReview)
# print(parser.get_format_instructions())
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a python code expert and reviewer. \n{format_instructions}"),
    ("user","Review this code.\n{code}")
]).partial(format_instructions = parser.get_format_instructions())


# final_prompt = prompt.invoke({"code":"a=10 b=0 print(a/b)"})
# print(final_prompt)

llm = ChatOllama(model = "qwen3:4b", temperature=0)

chain = prompt | llm  | parser
try:
    results = chain.invoke({
        "code" : "def divide(a, b): return a/b\nprint(divide(10, 0))"
    })
except Exception as e:
    print(f"Parsing failed: {e}")
# print(results.content)
print(results)