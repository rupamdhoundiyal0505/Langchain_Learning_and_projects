from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputParser,
    CommaSeparatedListOutputParser
)
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

# we have multiple output parsers in there all helps to decide how raw output 
# form a LLM is shown to us
# best is pydantic output parser

class MovieReview(BaseModel):
    title : str
    feedback : int
    summary : str


parser = PydanticOutputParser(pydantic_object=MovieReview)
# the above parser will attached in the chain that will model output of llm to object in this case it is MovieReview
# like this we have multiple parsers which we can use acc to our need


