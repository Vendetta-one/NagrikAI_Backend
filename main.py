from typing import TypedDict
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI



class NagrikState(TypedDict):
    # 1. The raw input from the citizen (Hindi/Hinglish/Audio transcript)
    original_input: str
    
    # 2. The normalized Bhashini translation
    translated_english: str
    
    # 3. Extracted variables: Location, Issue, Duration
    extracted_entities: dict
    
    # 4. Consensus Agent logic
    needs_clarification: bool
    follow_up_question: str
    
    # 5. Final Outputs for the Dashboard
    risk_level: str
    assigned_department: str


    # 1. Initialize the Brain (Gemini 1.5 Pro)
# We set temperature to 0.2 so it acts like a strict data extractor, not a creative writer.
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)

# 2. Define the First Agent: Ingestion Node
def node_ingestion(state: NagrikState):
    print("\n--- [NODE: INGESTION ACTIVATED] ---")
    
    # Grab the text from the state
    text = state.get("translated_english", "")
    
    # Strict prompt forcing JSON output
    prompt = f"""
    You are the Ingestion Agent for NagrikAI. 
    Analyze this citizen complaint: "{text}"
    Extract the following as a strict JSON object with exactly these keys:
    "Location", "Issue", "Duration".
    If a detail is missing, set its value to "UNKNOWN".
    Return ONLY raw JSON, without any markdown formatting or explanation.
    """
    
    # Ping Gemini
    response = llm.invoke(prompt)
    
    # Parse the response into a Python dictionary
    try:
        # Strip markdown ticks just in case Gemini tries to be helpful
        clean_json = response.content.replace("```json", "").replace("```", "").strip()
        entities = json.loads(clean_json)
    except Exception as e:
        print(f"Parsing Error: {e}")
        entities = {"Location": "UNKNOWN", "Issue": "UNKNOWN", "Duration": "UNKNOWN"}
        
    print(f"Extraction Complete: {entities}")
    
    # LangGraph Rule: Return ONLY the exact state variables we want to overwrite
    return {"extracted_entities": entities}

