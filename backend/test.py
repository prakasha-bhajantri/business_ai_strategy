from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


#------------- State -----------##
# Step 1: Define the "Clipboard" (State)
class LessonState(TypedDict):
    text: str

#-------------- Nodes -----------#
# Step 2: Define Node 1 (The Uppercaser)
def make_uppercase(state: LessonState):
    print("--- Executing Node 1 ---")
    current_text = state["text"]
    return {"text": current_text.upper()}  # Updates the state with uppercase text

# Step 3: Define Node 2 (The Greeter)
def add_greeting(state: LessonState):
    print("--- Executing Node 2 ---")
    current_text = state["text"]
    return {"text": f"Hello, {current_text}!"} # Prepends a greeting

#---------Connecint all together-----------
# Step 4: Build the Graph
workflow = StateGraph(LessonState)

# Add our workers
workflow.add_node("uppercase_node", make_uppercase)
workflow.add_node("greeting_node", add_greeting)

# Connect the flow: START -> Uppercase -> Greeting -> END
workflow.add_edge(START, "uppercase_node")
workflow.add_edge("uppercase_node", "greeting_node")
workflow.add_edge("greeting_node", END)

# Compile it!
app = workflow.compile()

# Step 5: Run it
final_state = app.invoke({"text": "john"})
print("\nFinal State Output:", final_state)




