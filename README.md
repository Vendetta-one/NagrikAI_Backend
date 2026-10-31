Live Demo Public URL: "https://lovable.dev/preview/wOJ5f89Xor7wtkfb0MDVEp2NlXhG1d3s"

# NagrikAI 🇮🇳

**Intelligent Civic Grievance Triage & Redressal System**
*Developed by Team Catalan for the JAI Hackathon 2026*

**Live Project URL:** [Insert Public URL Here]
**Demo Screen Recording:** [Insert Video Link Here]

---

## Overview

NagrikAI is a highly scalable, multi-agent AI backend designed to automate the triage of municipal grievances. By eliminating human bottlenecks in categorization, risk assessment, and departmental routing, NagrikAI processes unstructured, colloquial citizen complaints into standardized, actionable government tickets.

## System Architecture (Multi-Agent Pipeline)

The backend is powered by a stateless, asynchronous LangGraph `StateGraph` that manages a shared `NagrikState` across five specialized AI nodes:

1. **Ingestion Agent:** Parses unstructured natural language (including mixed Hindi/English) and extracts core entities (Location, Issue, Duration).
2. **Consensus Agent:** Acts as an automated spam filter and data validator. Evaluates if the provided information is sufficient to file a ticket. If not, it halts the pipeline and generates a natural language follow-up question for the citizen.
3. **Risk Assessment Agent:** Evaluates the severity of the extracted issue against a strict municipal rubric (High, Medium, Low) to determine Service Level Agreements (SLAs).
4. **Routing Agent:** Dynamically maps the grievance to the correct municipal department (e.g., PWD, Jal Board, Sanitation, Traffic Police).
5. **Vision Forensics Node (Hybrid):** Processes uploaded grievance images to detect synthetic AI-generated deepfakes and filter out fraudulent claims.
6. **Execution Sandbox:** Simulates a webhook gateway to a government portal, generating a mock official reference ID and success receipt without altering real-world production databases.

## Tech Stack & Third-Party Disclosures

In compliance with JAI Hackathon Technical Conduct rules (Rule T6), the following third-party components, APIs, and AI assistance tools are utilized in this project:

* **Core Frameworks:** Python, FastAPI, Pydantic, Uvicorn.
* **AI Orchestration:** LangGraph, LangChain (`langchain-google-genai`, `langchain-anthropic`).
* **Text Processing Pipeline:** Google Gemini (`gemini-3.5-flash`) via API for high-speed agentic routing and natural language understanding.
* **Vision & Image Forensics:** Anthropic Claude (`claude-3-5-sonnet-latest`) for advanced image verification.
* **Translation Services:** Bhashini API for localized Indian language processing.
* **AI Coding Assistance:** Generative AI tools were utilized during the hackathon for architectural scaffolding, LangGraph logic debugging, and boilerplate generation.

---

## Local Setup & Installation

**1. Clone the Repository**

```bash
git clone https://github.com/Vendetta-one/NagrikAI_Backend.git
cd NagrikAI_Backend

```

**2. Initialize the Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```

**3. Install Dependencies**

```bash
pip install fastapi uvicorn pydantic langgraph langchain-google-genai langchain-anthropic

```

**4. Set Environment Variables**
*Note: In compliance with Rule T8, API keys are never hardcoded or pushed to this repository.*

```bash
export GOOGLE_API_KEY="your_gemini_api_key_here"
export ANTHROPIC_API_KEY="your_claude_api_key_here"

```

**5. Launch the FastAPI Server**

```bash
uvicorn main:api_app --reload

```

The backend will launch at `[http://127.0.0.1:8000](http://127.0.0.1:8000)`.

---

## API Reference

### `POST /submit-ticket`

Processes a raw citizen grievance and triggers the LangGraph multi-agent pipeline.

**Request Body (JSON):**

```json
{
    "original_input": "bhai sector 16 ke paas main road pe bohot bada gadha ho gaya hai, accident ho rahe hain kal se",
    "translated_english": "There is a very large pothole on the main road near Sector 16, accidents have been happening since yesterday."
}

```

**Successful Response (200 OK):**

```json
{
    "status": "success",
    "department": "Public Works Department (PWD) (Ref: NAGRIK-2026-90412)",
    "risk_level": "Medium",
    "entities": {
        "Location": "main road near Sector 16",
        "Issue": "very large pothole"
    }
}

```

**Clarification Response (If AI requires more information):**

```json
{
    "status": "needs_info",
    "follow_up": "Could you please specify the exact landmark near Sector 16?"
}

```
