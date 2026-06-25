from typing import final
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

# The four Runnable methods you should know

# .invoke(input)Run once, return one result. Most common.
# .stream(input)Stream tokens as they come — for real-time UI
# .batch([input1, input2])Run multiple inputs in parallel
# .ainvoke(input)Async version of invoke — for FastAPI etc.

# Method 1:
# Use direct constructor


# pt = PromptTemplate(
#     input_variables=["topic"],
#     template=f"Explain {topic} in simple terms"
# )

# Method 2
# using from_template <- preferred

pt = PromptTemplate.from_template("Explain {topic} in simple words!!")

# Invoke return a StringPromptValue that will be fed to the llm

final_prompt = pt.invoke({"topic":"recursion"})
# pt.format(topic = "recursion")
# print(final_prompt)



# ChatPromptTemplate

chat_pt = ChatPromptTemplate.from_messages([
    ("system" , "You are a helpful {role}"),
    ("human" , "Answer this{question}")
])


final_chat_pt  = chat_pt.invoke({
    "role" : "Python tutor",
    "question" : "What is decorator?"
})

# print(final_chat_pt)


# Partial Prompts
translator = PromptTemplate.from_template(
    "Translate the following to {language} : {text}"
)

french = translator.partial(language = "French")
prompt = french.invoke({
    "text" : "What is RTL"
})
# print(prompt)




import datetime
dated_prompt = PromptTemplate.from_template(
    "Today is {date}. {question}"
).partial(date = lambda: datetime.date.today().isoformat())

# print(dated_prompt.invoke({"question": "How MOS works!"}))


# ***********MessagePlaceholder****************

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Electrical engineer"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chat_prompt = prompt.invoke({
    "history" : [HumanMessage("Hi"),AIMessage("Hello!")],
    "input" : "What are you best at!!"
})

# print(HumanMessage("hi"), AIMessage("hello"))
print(chat_prompt)