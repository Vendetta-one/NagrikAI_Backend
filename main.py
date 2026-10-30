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

# 3. Define the Second Agent: Consensus Node
def node_consensus(state: NagrikState):
    print("\n--- [NODE: CONSENSUS ACTIVATED] ---")
    
    entities = state.get("extracted_entities", {})
    location = entities.get("Location", "UNKNOWN")
    issue = entities.get("Issue", "UNKNOWN")
    
    # Check if core details are missing
    if location == "UNKNOWN" or issue == "UNKNOWN":
        print("Missing critical information! Triggering clarification flow...")
        
        prompt = f"""
        You are the Consensus Agent for NagrikAI. 
        A citizen reported an issue, but critical details are missing.
        Current details extracted: {entities}
        Generate ONE polite, concise follow-up question asking ONLY for the missing detail(s).
        Keep it under 20 words and do not ask for redundant information.
        """
        
        response = llm.invoke(prompt)
        return {
            "needs_clarification": True,
            "follow_up_question": response.content.strip()
        }
    else:
        print("All core details present. Proceeding downstream...")
        return {
            "needs_clarification": False,
            "follow_up_question": ""
        }
    
    # 4. Define the Third Agent: Risk Assessment Node
def node_risk(state: NagrikState):
    print("\n--- [NODE: RISK ASSESSMENT ACTIVATED] ---")
    
    # Grab the specific issue from the state memory
    issue = state.get("extracted_entities", {}).get("Issue", "UNKNOWN")
    
    # Strict prompt forcing a single-word classification
    prompt = f"""
    You are the Risk Assessment Agent for NagrikAI.
    Evaluate the severity of this citizen issue: "{issue}"
    Classify it strictly into one of three categories: "High", "Medium", or "Low".
    
    - High: Imminent danger to life/property (e.g., open live wires, major water pipe bursts).
    - Medium: Significant inconvenience (e.g., deep potholes, sustained power cuts).
    - Low: Minor issues (e.g., non-functioning streetlights, daily garbage accumulation).
    
    Return ONLY the single word: High, Medium, or Low. Do not include punctuation.
    """
    
    # Ping Gemini
    response = llm.invoke(prompt)
    risk = response.content.strip()
    
    # Safety fallback in case the model hallucinates extra text
    if risk not in ["High", "Medium", "Low"]:
        risk = "Medium"
        
    print(f"Assessed Risk Level: {risk}")
    
    # Update the global state
    return {"risk_level": risk}

# 5. Define the Fourth Agent: Routing Node
def node_routing(state: NagrikState):
    print("\n--- [NODE: ROUTING ACTIVATED] ---")
    
    # Grab the issue and location from state memory
    entities = state.get("extracted_entities", {})
    issue = entities.get("Issue", "UNKNOWN")
    location = entities.get("Location", "UNKNOWN")
    
    # Strict prompt forcing exact department matching
    prompt = f"""
    You are the Routing Agent for NagrikAI.
    A citizen from "{location}" has reported this issue: "{issue}"
    Assign this grievance strictly to the most appropriate municipal department from this list:
    - Public Works Department (PWD)
    - Electricity Board
    - Jal Board (Water & Sewage)
    - Sanitation Department
    - Traffic Police
    - General Municipal Administration
    
    Return ONLY the name of the department exactly as written in the list above. 
    Do not include any explanation or punctuation.
    """
    
    # Ping Gemini
    response = llm.invoke(prompt)
    department = response.content.strip()
    
    print(f"Assigned Department: {department}")
    
    # Update the global state
    return {"assigned_department": department}

    # 6. Define the Final Execution Agent
def node_execution(state: NagrikState):
    print("\n--- [NODE: EXECUTION ACTIVATED] ---")
    
    # 1. Gather the finalized data from the state
    payload = {
        "location": state.get("extracted_entities", {}).get("Location", "UNKNOWN"),
        "issue": state.get("extracted_entities", {}).get("Issue", "UNKNOWN"),
        "risk_level": state.get("risk_level", "UNKNOWN"),
        "department": state.get("assigned_department", "UNKNOWN")
    }
    
    print(f"Dispatching payload to {payload['department']} API Gateway...")
    
    # 2. Simulate the Government Portal Response for the Demo
    gov_response = {
        "status": "FILED_SUCCESSFULLY",
        "gov_reference_id": "NAGRIK-2026-90412",
        "sla_resolution_hours": 48 if payload['risk_level'] == "High" else 120
    }
    
    # 3. Print the final Hackathon Demo UI in the terminal
    print("\n==================================================")
    print("✅ OFFICIAL TICKET SUCCESSFULLY CREATED")
    print("==================================================")
    print(f"Reference ID : {gov_response['gov_reference_id']}")
    print(f"Department   : {payload['department']}")
    print(f"Risk Level   : {payload['risk_level']} (SLA: {gov_response['sla_resolution_hours']} Hours)")
    print(f"Location     : {payload['location']}")
    print(f"Issue        : {payload['issue']}")
    print("==================================================\n")
    
    # Update state with the final reference ID appended
    return {"assigned_department": f"{payload['department']} (Ref: {gov_response['gov_reference_id']})"}