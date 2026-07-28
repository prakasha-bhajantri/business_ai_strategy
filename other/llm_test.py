import os
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

# Load variables from .env file into os.environ
load_dotenv()

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver  # <-- NEW: Import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI

api_key = os.getenv("GEMINI_API_KEY")

# 1. Initialize the Gemini model using your API key
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash", 
    api_key=api_key,
    temperature=0.7
)

# 2. Define the State structure. 
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Create the chatbot node
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 4. Build the Graph
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph_builder.add_edge("chatbot", END)

# 5. Add Memory persistence so thread_id actually works
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)  # <-- NEW: Pass memory here

# --- Execution ---

config = {"configurable": {"thread_id": "1"}}

print("--- First Turn ---")
events = graph.stream(
    {"messages": [("user", "Hi, my name is John.")]}, 
    config
)

for event in events:
    if "chatbot" in event:
        print("Assistant:", event["chatbot"]["messages"][-1].content)

print("\n--- Second Turn ---")
events_followup = graph.stream(
    {"messages": [("user", "What is my name?")]}, 
    config
)

for event in events_followup:
    if "chatbot" in event:
        print("Assistant:", event["chatbot"]["messages"][-1].content)



# Langgraph


