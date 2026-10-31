# NagrikAI 

*Intelligent Civic Grievance Triage & Redressal System*[cite: 1]
Developed by Team Catalan for the JAI Hackathon 2026[cite: 1]

*Live Demo Public URL:* "https://lovable.dev/preview/wOJ5f89Xor7wtkfb0MDVEp2NlXhG1d3s"[cite: 2]
*Demo Screen Recording:* [Insert Video Link Here][cite: 1]

## Overview[cite: 1]

NagrikAI is a highly scalable, multi-agent AI backend designed to automate the triage of municipal grievances[cite: 1]. By eliminating human bottlenecks in categorization, risk assessment, and departmental routing, NagrikAI processes unstructured, colloquial citizen complaints into standardized, actionable government tickets[cite: 1].

## System Architecture (Multi-Agent Pipeline)[cite: 1]

The backend is powered by a stateless, asynchronous LangGraph StateGraph that manages a shared NagrikState across five specialized AI nodes:[cite: 1]

* *Node 1: Multilingual Ingestion (Agora STT)*: Captures real-time voice input from the citizen via the frontend, transcribing regional dialects and translating them into standard English.
* *Node 2: Categorization Agent*: Analyzes the transcribed text and maps the grievance to the correct municipal domain (e.g., Infrastructure, Sanitation, Water Supply).
* *Node 3: Risk & Urgency Assessor*: Evaluates the severity of the issue based on context (e.g., a massive pothole causing accidents vs. a flickering streetlight) and assigns a priority tier.
* *Node 4: Department Routing*: Determines the precise government or municipal department responsible for execution.
* *Node 5: Ticket Generation*: Compiles the processed data into an official ticket ready for rendering on the civic dashboard.

## Tech Stack

* *Frontend Environment*: React / Lovable 
* *Voice Integration*: Agora Voice SDK / Web Speech API
* *Backend Framework*: Python, FastAPI, Uvicorn
* *AI Orchestration*: LangGraph, LangChain
* *Tunneling / Connectivity*: localtunnel / ngrok

## API Reference

### Submit a Citizen Grievance
```http
POST /submit-ticket


REQUEST PAYLOAD

{
  "original_input": "string (transcribed text from Agora)",
  "translated_english": "string"
}


SUCCESS RESPONSE

{
  "status": "success",
  "department": "Public Works Department",
  "risk_level": "High",
  "entities": ["Sector 16", "Main Road"]
}



MISSING INFORMATION/FOLLOW-UP RESPONSE

{
  "status": "needs_info",
  "follow_up": "AI generated follow-up question asking the citizen for clarification (e.g., exact landmark)."
}
