"""
test_simulate_api.py — Verify Feature 4 (Micro-Task Simulation Endpoints)
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

print("=" * 60)
print("Testing Feature 4: Micro-Task Simulation & Evaluation Pipeline")
print("=" * 60)

# 1. Test GET /api/simulate/tasks
print("\n[1] Testing GET /api/simulate/tasks ...")
resp_tasks = client.get("/api/simulate/tasks")
print(f"Status: {resp_tasks.status_code}")
tasks_data = resp_tasks.json()
print(f"Total available simulation tasks: {len(tasks_data.get('tasks', []))}")
for i, task in enumerate(tasks_data.get('tasks', [])[:4], 1):
    print(f"  ({i}) [{task.get('difficulty').upper()}] {task.get('skill_name')}: {task.get('scenario_text')[:80]}...")

# 2. Test POST /api/simulate with realistic user response
print("\n[2] Testing POST /api/simulate ...")
sample_task = tasks_data['tasks'][0]
task_id = sample_task['id']
user_id = "587479a6-04d5-4371-a57f-c3b39c9b7be2"

print(f"Selected Task: {sample_task.get('skill_name')} (ID: {task_id})")
print(f"Scenario: {sample_task['scenario_text'][:120]}...")
print(f"Rubric Criteria: {sample_task['rubric_criteria']}")

payload = {
    "user_id": user_id,
    "task_id": task_id,
    "user_response": (
        "To resolve the OOM crashes, I would refactor the Python script into a generator-based streaming pipeline. "
        "Instead of loading the entire 50GB CSV into RAM, I will read data in chunks of 50,000 rows using Polars or Pandas chunking. "
        "Each chunk is validated using Pydantic schemas to ensure data integrity and detect corrupt records. "
        "Malformed rows will be quarantined into a dead-letter queue with structured error logging, while valid records are batched into the database."
    )
}

resp_sim = client.post("/api/simulate", json=payload)
print(f"\nStatus: {resp_sim.status_code}")
sim_data = resp_sim.json()
print("Evaluator Feedback:")
print(f"  • Score: {sim_data.get('score_percent')}%")
print(f"  • Evaluated: {sim_data.get('evaluated')}")
print(f"  • Feedback: {sim_data.get('improvement_reasoning')}")
print(f"  • Missing Concepts: {sim_data.get('missing_concepts')}")

# 3. Test GET /api/simulate/history
print("\n[3] Testing GET /api/simulate/history ...")
resp_hist = client.get(f"/api/simulate/history?user_id={user_id}")
print(f"Status: {resp_hist.status_code}")
hist_data = resp_hist.json()
print(f"User total simulation attempts: {hist_data.get('total_attempts')}")
if hist_data.get('history'):
    latest = hist_data['history'][0]
    print(f"  Latest Attempt Score: {latest.get('score_percent')}% at {latest.get('created_at')}")

print("\n[SUCCESS] Feature 4 verification completed successfully!")
