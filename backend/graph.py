import os
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

#------------- State -----------##
# Step 1: Define the "Clipboard" (State)
class RentalPlannerState(TypedDict):
    question: str
    classifier:str
    location_analysis:str
    rental_analysis:str
    agreement_analysis:str
    fallback:str

api_key = os.getenv("GEMINI_API_KEY")

# 1. Initialize the Gemini model using your API key
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash", 
    api_key=api_key,
    temperature=0
)

# Function to call the llm with custom prompt
def llm_call(prompt):
    response = llm.invoke(prompt)
    
    # If content is a list of block dictionaries (e.g., [{'type': 'text', 'text': 'rent', ...}])
    if isinstance(response.content, list):
        text_parts = [
            block["text"] for block in response.content 
            if isinstance(block, dict) and "text" in block
        ]
        return "".join(text_parts).strip()
    
    # Standard string fallback
    return str(response.content).strip()

#-------------- Nodes -----------#
# Step 1: Define Node 1 - queryclassifier
def queryClassifier(state: RentalPlannerState):
    print("--- Executing Node 1 : queryclassifier ---")
    question = state["question"]
    QUERY_CLASSIFIER_PROMPT = f"""
You are an automated assistant for a property rental service.
Categorize the user's inquiry into one of these exact types:
- location: Questions about location, areas.
- rent: Questions about rent prices or rent ranges or rent yields.
- agreement: Questions about agreements, policies
- fallback: Any irrelevant questions

Question: {question}

Output:
Return ONLY one word from: 'location', 'rent', 'agreement', 'fallback'. Do not include markdown or punctuation.
"""
    classifier = llm_call(QUERY_CLASSIFIER_PROMPT)
    if classifier in ['location', 'rent', 'agreement', 'fallback']:

        return {"classifier": classifier}  # Updates the state with uppercase text
    else:
        return {"classifier": 'InvalidClassifier'} 



# Step 1: Define Node 2 - locationAnalyzer
def locationAnalyzer(state: RentalPlannerState):
    print("--- Executing Node 1 : locationAnalyzer ---")
    question = state["question"]
    LOCATION_ANALYZER_PROMPT = f"""
You are an expert property rental assistant specializing in location and neighborhood analysis.

### Task
Analyze the user's question, identify the location mentioned, and provide a helpful, accurate answer.

### Instructions
1. Identify the specific city, neighborhood, or region in the user's question.
2. Answer the user's request regarding that location (e.g., area overview, accessibility, lifestyle, or general rental context).
3. Do not invent facts or guess. If you do not have reliable information about the location or cannot answer the question, reply strictly with: "I don't know!"

### Output Format
- Provide ONLY the direct response (no preamble like "Sure, here is...").
- Format the response in clear, well-structured paragraphs.

Question: {question}
"""
    analysis = llm_call(LOCATION_ANALYZER_PROMPT)

    return {"location_analysis": analysis}  # Updates the state with uppercase text


# Step 1: Define Node 3 - rentalAnalyzer
def rentalAnalyzer(state: RentalPlannerState):
    print("--- Executing Node 2 : rentalAnalyzer ---")
    question = state["question"]
    RENTAL_ANALYZER_PROMPT = f"""
You are an expert property rental analyst specializing in rental pricing, market trends, and lease costs.

### Task
Analyze the user's question regarding rental property pricing, costs, or market estimates, and provide an accurate analysis.

### Instructions
1. Extract key details from the question (e.g., apartment configuration like 1BHK/2BHK, target location, and budget constraints).
2. Provide a clear rental analysis covering expected rent ranges, security deposits, or typical market conditions relevant to the query.
3. Do not invent pricing or make wild guesses. If you lack reliable market data or the query cannot be answered accurately, reply strictly with: "I don't know!"

### Output Format
- Provide ONLY the direct rental analysis (no preamble like "Sure, here is your analysis:").
- Format the response in clear, well-structured paragraphs.
- Highlight price estimates or key numerical figures clearly using standard currency formatting.

Question: {question}
"""
    analysis = llm_call(RENTAL_ANALYZER_PROMPT)

    return {"rental_analysis": analysis}  # Updates the state with uppercase text

# Step 1: Define Node 4 - aggrementAnalyzer
def agreementAnalyzer(state: RentalPlannerState):
    print("--- Executing Node 4 : aggrementAnalyzer ---")
    question = state["question"]
    AGREEMENT_ANALYZER_PROMPT = f"""
You are an expert property rental assistant specializing in lease agreements, rental policies, and tenancy terms.

### Task
Analyze the user's question regarding lease terms, policies, or rental agreements, and provide a clear, legally grounded, and accurate answer.

### Instructions
1. Identify the core policy or clause in the user's query (e.g., lock-in period, notice duration, security deposit refund rules, pet policy, subletting, or maintenance responsibilities).
2. Explain the standard terms, typical clauses, or specific agreement details requested.
3. Highlight potential edge cases or critical conditions (e.g., penalties for early termination or breach of contract).
4. Do not speculate or make up policy details. If you lack accurate information or the question requires specific legal review of an unprovided document, reply strictly with: "I don't know!"

### Output Format
- Provide ONLY the direct response (no preamble like "Sure, here is the information:").
- Format the response in clear, well-structured paragraphs.
- Use bold text for key legal terms, clauses, or timelines (e.g., **30-day notice period**, **lock-in clause**).

Question: {question}
"""
    analysis = llm_call(AGREEMENT_ANALYZER_PROMPT)

    return {"agreement_analysis": analysis}  # Updates the state with uppercase text

# Step 1: Define Node 4 - fallback
def fallback(state: RentalPlannerState):
    print("--- Executing Node 5 : fallback ---")

    response = f""" Hey!, Thanks for asking, But I am not trained to answer this question, 
please ask any question related to Housing Rental Planning.
"""

    return {"fallback": response}  # Updates the state with uppercase text


# Step 2: Define Routes
def route_by_classifier(state: RentalPlannerState):
    print("--- Executing : Router ---")
    classifier = state.get("classifier", "fallback")
    mapping = {
        "location":"locationAnalyzer",
        "rent":"rentalAnalyzer",
        "agreement":"agreementAnalyzer",
        "fallback":"fallback"
    }

    return mapping.get(classifier, "fallback")


#---------Connecint all together-----------
# Step 4: Build the Graph
workflow = StateGraph(RentalPlannerState)

# Add nodes
workflow.add_node("queryClassifier", queryClassifier)
workflow.add_node("locationAnalyzer", locationAnalyzer)
workflow.add_node("rentalAnalyzer", rentalAnalyzer)
workflow.add_node("agreementAnalyzer", agreementAnalyzer)
workflow.add_node("fallback", fallback)

# Connect the flow with the edges
workflow.add_edge(START, "queryClassifier")

# Add conditional Edge
workflow.add_conditional_edges("queryClassifier",
                               route_by_classifier,
                               {
                                "locationAnalyzer":"locationAnalyzer",
                                "rentalAnalyzer":"rentalAnalyzer",
                                "agreementAnalyzer":"agreementAnalyzer",
                                "fallback":"fallback"
                               }
 )


workflow.add_edge("locationAnalyzer", END)
workflow.add_edge("rentalAnalyzer", END)
workflow.add_edge("agreementAnalyzer", END)
workflow.add_edge("fallback", END)

# Compile it!
app = workflow.compile()

# Step 5: Run it
if __name__ == "__main__":
    test_question = {
        "question": "which agreement i should make for renting an house in tokyo"
    }

    print("\n Starting the Langgraph")
    result = app.invoke(test_question)

    print("\n--- Final Graph State ---")
    print(f"Classifier Chosen : {result.get('classifier')}\n")

    # Print the specific analysis that was generated
    if "location_analysis" in result:
        print(f"Location Analysis:\n{result['location_analysis']}")
    elif "rental_analysis" in result:
        print(f"Rental Analysis:\n{result['rental_analysis']}")
    elif "agreement_analysis" in result:
        print(f"Agreement Analysis:\n{result['agreement_analysis']}")
    elif "fallback" in result:
        print(f"Fallback Response:\n{result['fallback']}")
