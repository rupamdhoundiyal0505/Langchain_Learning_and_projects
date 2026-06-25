from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from pydantic import BaseModel ,Field

parser = JsonOutputParser()
print(parser.get_format_instructions())



class MovieReview (BaseModel):
    name : str = Field(description="write name here")


parser = PydanticOutputParser(pydantic_object=MovieReview)

print(parser.get_format_instructions())
