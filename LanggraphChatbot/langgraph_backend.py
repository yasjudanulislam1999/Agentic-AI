import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from pydantic import BaseModel,Field
from typing import TypedDict, Literal, Annotated
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="gemma2-9b-it")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {'messages': [response]}

from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
config = {'configurable': {'thread_id':1}}

graph = StateGraph(ChatState)

graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer=checkpointer)

