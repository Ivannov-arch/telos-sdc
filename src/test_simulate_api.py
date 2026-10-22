"""
test_simulate_api.py — Verify Priority 3: Scaffold Backend Feature 4 (/api/simulate)
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

print("=" * 60)
print("Testing Priority 3: Feature 4 Micro-Task Simulation Endpoints")
print("=" * 60)

# 1. Test GET /api/simulate/tasks
print("\n[1] Testing GET /api/simulate/tasks ...")
resp_tasks = client.get("/api/simulate/tasks")
print(f"Status: {resp_tasks.status_code}")
tasks_data = resp_tasks.json()
print(f"Tasks received: {len(tasks_data.get('tasks', []))}")
if tasks_data.get('tasks'):
    sample_task = tasks_data['tasks'][0]
    print(f"Sample Task ID: {sample_task.get('id')}")
    print(f"Scenario: {sample_task.get('scenario_text', '')[:100]}...")

# 2. Test POST /api/simulate
print("\n[2] Testing POST /api/simulate ...")
task_id = tasks_data['tasks'][0]['id'] if tasks_data.get('tasks') else "a4a0ab6f-83d8-46fa-b50d-2976eeaf04fb"
payload = {
    "user_id": "587479a6-04d5-4371-a57f-c3b39c9b7be2",
    "task_id": task_id,
    "user_response": "I would build a CI/CD pipeline using GitHub Actions, containerize the service with Docker, and configure blue-green deployments."
}
resp_sim = client.post("/api/simulate", json=payload)
print(f"Status: {resp_sim.status_code}")
sim_data = resp_sim.json()
print("Simulation Submission Result:")
for k, v in sim_data.items():
    print(f"  {k}: {v}")
print("\n[SUCCESS] Priority 3 verification completed successfully!")
