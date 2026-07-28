import os
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

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

# question = "what is the rent in tokyo central town for 1 bhk house"
question = "which area/location best for renting in tokyo?"
# question = "which agreement i should make for renting an house in tokyo"
# question = "who is president of Japan"

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
# classifier = query_classifier_llm(QUERY_CLASSIFIER_PROMPT)


question = "which area/location best for renting in tokyo?"


# prompt
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

# response = llm_call(LOCATION_ANALYZER_PROMPT)
# print(response)

question = "what is the rent in tokyo central town for 1 bhk house"

# prompt
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

# response = llm_call(RENTAL_ANALYZER_PROMPT)
# print(response)


question = "which agreement i should make for renting an house in tokyo"

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


response = llm_call(AGREEMENT_ANALYZER_PROMPT)
print(response)






