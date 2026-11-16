# Offshore Operations & Zero-Harm Safety Agentic AI

A multi-agent Python prototype built with **CrewAI** and **Google Gemini** demonstrating automated retrieval, physical unit conversion, and safety compliance auditing for offshore energy maintenance workflows.

## Architecture & Workflow
1. **Retrieval Context (`safety_manual.txt`):** Loads operational thresholds, lockout/tagout limits, and PPE requirements for hydraulic pumps, offshore wind turbines (Hywind), and subsea pipelines.
2. **Offshore Maintenance Planner Agent:** Evaluates incoming technician requests, performs unit conversions (PSI to bar, knots to m/s), and drafts a safety checklist.
3. **Zero-Harm Safety & Physics Auditor Agent:** Independently verifies all mathematical calculations, pressure drop tolerances, and safety rules before issuing an `[APPROVED]` or `[REJECTED]` status.

## How to Run
1. Install dependencies: `pip install crewai google-genai`
2. Set your Gemini API key in `safety_agent.py`
3. Run the evaluation suite: `python safety_agent.py`