"""
test_render_cloud.py — Live End-to-End Test Suite against Render Cloud URL
Target: https://telos-sdc.onrender.com
"""

import json
import requests
import time

BASE_URL = "https://telos-sdc.onrender.com"

def print_section(title):
    print("\n" + "=" * 75)
    print(f" {title}")
    print("=" * 75)

def print_io(name, method, endpoint, input_data, status_code, output_data, elapsed_s):
    print(f"\n▶ TEST: {name}")
    print(f"  URL: {method} {BASE_URL}{endpoint}")
    print(f"  Latency: {elapsed_s:.2f}s")
    if input_data is not None:
        print("  [INPUT]:")
        print("  " + json.dumps(input_data, indent=4).replace("\n", "\n  "))
    else:
        print("  [INPUT]: None (Query params in URL)")
    print(f"  [STATUS CODE]: {status_code}")
    print("  [OUTPUT]:")
    print("  " + json.dumps(output_data, indent=4).replace("\n", "\n  "))

def run_tests():
    print_section(f"RUNNING LIVE CLOUD TEST ON {BASE_URL}")

    # 1. Healthcheck
    t0 = time.time()
    r1 = requests.get(f"{BASE_URL}/health", timeout=30)
    print_io(
        name="1. Health Check",
        method="GET",
        endpoint="/health",
        input_data=None,
        status_code=r1.status_code,
        output_data=r1.json(),
        elapsed_s=time.time() - t0,
    )

    # 2. Profiles list
    t0 = time.time()
    r2 = requests.get(f"{BASE_URL}/api/profiles", timeout=30)
    d2 = r2.json() if r2.status_code == 200 else {"raw": r2.text}
    sample_profiles = d2.get("profiles", []) if isinstance(d2, dict) else []
    demo_user_id = sample_profiles[0]["id"] if sample_profiles else "146f103d-946f-4619-9fa0-ba0b4fdfe84c"
    print_io(
        name="2. Demo User Profiles List",
        method="GET",
        endpoint="/api/profiles",
        input_data=None,
        status_code=r2.status_code,
        output_data={
            "total_profiles_returned": len(sample_profiles),
            "sample_profile_id": demo_user_id,
            "sample_profile": sample_profiles[0] if sample_profiles else None,
        },
        elapsed_s=time.time() - t0,
    )

    # 3. Matching — Moderate Scenario
    t0 = time.time()
    endpoint_match_mod = f"/api/match?user_id={demo_user_id}&scenario=moderate&top_k=2"
    r3 = requests.get(f"{BASE_URL}{endpoint_match_mod}", timeout=30)
    d3 = r3.json() if r3.status_code == 200 else {"raw": r3.text}
    print_io(
        name="3. Role Match (Scenario: Moderate)",
        method="GET",
        endpoint=endpoint_match_mod,
        input_data=None,
        status_code=r3.status_code,
        output_data=d3,
        elapsed_s=time.time() - t0,
    )

    # 4. Matching — Fast Scenario (Disruption Stress-Test)
    t0 = time.time()
    endpoint_match_fast = f"/api/match?user_id={demo_user_id}&scenario=fast&top_k=2"
    r4 = requests.get(f"{BASE_URL}{endpoint_match_fast}", timeout=30)
    d4 = r4.json() if r4.status_code == 200 else {"raw": r4.text}
    print_io(
        name="4. Role Match (Scenario: Fast AI Disruption Stress-Test)",
        method="GET",
        endpoint=endpoint_match_fast,
        input_data=None,
        status_code=r4.status_code,
        output_data=d4,
        elapsed_s=time.time() - t0,
    )

    # 5. Simulation Tasks List
    t0 = time.time()
    r5 = requests.get(f"{BASE_URL}/api/simulate/tasks", timeout=30)
    d5 = r5.json() if r5.status_code == 200 else {"raw": r5.text}
    tasks = d5.get("tasks", []) if isinstance(d5, dict) else []
    sample_task = tasks[0] if tasks else None
    print_io(
        name="5. Micro-Task Simulation Scenarios List",
        method="GET",
        endpoint="/api/simulate/tasks",
        input_data=None,
        status_code=r5.status_code,
        output_data={
            "total_tasks_available": d5.get("count", len(tasks)),
            "first_sample_task": sample_task,
        },
        elapsed_s=time.time() - t0,
    )

    # 6. Post Simulation Submission
    t0 = time.time()
    task_id = sample_task["id"] if sample_task else "a4a0ab6f-83d8-46fa-b50d-2976eeaf04fb"
    sim_payload = {
        "user_id": demo_user_id,
        "task_id": task_id,
        "user_response": (
            "To build this architecture, I will implement a modular pipeline with streaming generators. "
            "Data is read in chunks to prevent memory overhead, validated using strict Pydantic schemas, "
            "and routed to a dead-letter queue when malformed. I evaluated trade-offs between memory footprint "
            "and latency, ensuring high resilience and unit-testable components."
        )
    }
    r6 = requests.post(f"{BASE_URL}/api/simulate", json=sim_payload, timeout=30)
    d6 = r6.json() if r6.status_code == 200 else {"raw": r6.text}
    print_io(
        name="6. Submit Simulation Task Evaluation",
        method="POST",
        endpoint="/api/simulate",
        input_data=sim_payload,
        status_code=r6.status_code,
        output_data=d6,
        elapsed_s=time.time() - t0,
    )

    # 7. Simulation History (KPI Tracking)
    t0 = time.time()
    endpoint_hist = f"/api/simulate/history?user_id={demo_user_id}"
    r7 = requests.get(f"{BASE_URL}{endpoint_hist}", timeout=30)
    d7 = r7.json() if r7.status_code == 200 else {"raw": r7.text}
    print_io(
        name="7. Simulation History (Skill Gap Reduction KPI)",
        method="GET",
        endpoint=endpoint_hist,
        input_data=None,
        status_code=r7.status_code,
        output_data={
            "user_id": demo_user_id,
            "total_attempts": d7.get("total_attempts") if isinstance(d7, dict) else 0,
            "latest_attempt": d7.get("history", [])[0] if isinstance(d7, dict) and d7.get("history") else None,
        },
        elapsed_s=time.time() - t0,
    )

    print_section("RENDER CLOUD TEST SUITE FINISHED!")

if __name__ == "__main__":
    run_tests()
