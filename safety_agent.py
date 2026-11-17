import os
from crewai import Agent, Task, Crew, Process

# AQ.
os.environ["GEMINI_API_KEY"] = "GEMINI_API_KEY"


with open("safety_manual.txt", "r", encoding="utf-8") as file:
    manual_text = file.read()


planner_agent = Agent(
    role="Offshore Maintenance Planner",
    goal="Draft a clear step-by-step maintenance checklist based strictly on the company safety manual.",
    backstory="You are an operations engineer who prepares work orders for offshore technicians.",
    llm="gemini/gemini-3.8-flash",
    verbose=True
)


auditor_agent = Agent(
    role="Zero-Harm Safety & Physics Auditor",
    goal="Verify that all pressure, temperature, wind limits, and safety gear match the manual.",
    backstory="You are a strict safety officer. You check every number and unit conversion to prevent accidents.",
    llm="gemini/gemini-3.8-flash",
    verbose=True
)


test_scenarios = [
    "Scenario 1 (Pump P-104): Technician wants to open a valve. Current readings: Pressure = 290 PSI, Temperature = 38°C.",
    "Scenario 2 (Wind Turbine WT-09): Technician wants to do exterior blade inspection. Wind speed is 26 knots.",
    "Scenario 3 (Pipeline S-42): Hydrotest started at 200 bar. After 4 hours, pressure is 198.4 bar. Can we certify the pipeline?"
]

for scenario in test_scenarios:
    print(f"\n--- RUNNING TEST: {scenario} ---\n")
    
    plan_task = Task(
        description=(
            f"Using this safety manual:\n{manual_text}\n\n"
            f"Evaluate this request: '{scenario}'. "
            "Convert all units carefully (1 bar = 14.5 PSI, 1 m/s = 1.944 knots) and list required PPE."
        ),
        expected_output="Step-by-step physics/unit check and safety recommendation.",
        agent=planner_agent
    )

    audit_task = Task(
        description=(
            "Audit the Maintenance Planner's math and safety logic against the manual. "
            "Check if 290 PSI > 2 bar, if 26 knots > 12 m/s, and if a 1.6 bar drop exceeds 0.5% of 200 bar. "
            "End with a clear status: [APPROVED] or [REJECTED]."
        ),
        expected_output="Verification report with exact math check and final [APPROVED] or [REJECTED] badge.",
        agent=auditor_agent
    )

    crew = Crew(
        agents=[planner_agent, auditor_agent],
        tasks=[plan_task, audit_task],
        process=Process.sequential
    )
    
    print(crew.kickoff())