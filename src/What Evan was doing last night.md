# ############################################################
# PLEASE DELETE AFTER READING THIS
# ############################################################

## Summary of Work Done & Issues Resolved

### 1. What Happened Behind the Scenes
When testing **Priority 2 (Live Hybrid Search)** and **Priority 3 (Simulation Endpoint)**, the code encountered two blocking bugs that had to be fixed:

1. **User Profiles Had No Vectors (`NULL`):**
   - The synthetic profiles in `telos_sdc.user_profiles` were created with `user_dense_vector = NULL`.
   - Because of this, `match.py` was forced into the hardcoded skill fallback instead of executing live hybrid search.
   - **Fix:** Ran `src/supabase/embed_user_profiles.py` to embed all 14 profiles via your active RunPod BGE-M3 endpoint so each profile now has a real 1024-dim dense vector.

2. **Supabase PostgREST RPC Schema Error:**
   - In `src/backend/routers/match.py`, the code was calling `db.rpc("telos_sdc.hybrid_search", ...)`.
   - PostgREST looked for the function inside the `public` schema and threw error `PGRST202 (function not found in schema cache)`.
   - **Fix:** Changed the call to `db.schema("telos_sdc").rpc("hybrid_search", ...)`.

3. **Missing Starter Task for `/api/simulate`:**
   - The `telos_sdc.simulation_tasks` table was empty, causing `POST /api/simulate` to return 404.
   - **Fix:** Seeded one sample task (`a4a0ab6f-83d8-46fa-b50d-2976eeaf04fb`) into `telos_sdc.simulation_tasks` so the endpoint can be submitted to and validated.

---

### 2. Files Modified / Created

| File | Status | Description |
|---|---|---|
| `src/backend/routers/match.py` | Modified | Fixed schema RPC call so live `hybrid_search()` runs with dense vectors. |
| `src/backend/routers/simulate.py` | Modified | Fixed `maybe_single()` return check to safely handle missing rows. |
| `src/supabase/embed_user_profiles.py` | Created | Helper that embedded the 14 synthetic profiles into `telos_sdc.user_profiles`. |
| `src/test_match_api.py` | Created | Standalone test script for Priority 2 (`GET /api/match`). |
| `src/test_simulate_api.py` | Created | Standalone test script for Priority 3 (`GET & POST /api/simulate`). |

---

### 3. Verification & Test Results

#### Priority 1: Role Vectors (Done by You)
- 1,000 ESCO occupation vectors generated and saved in `telos_sdc.role_vectors`.

#### Priority 2: Live Hybrid Search (`test_match_api.py`)
- **Status:** HTTP 200 (Success)
- **AI/NLP User Profile:** Matched **Computer Scientist**, **Data Analyst**, **Software Developer**.
- **Data Engineering Profile:** Matched **Data Engineer** (Rank 1).
- Fallback was bypassed; candidate selection used real cosine similarity + RRF ranks.

#### Priority 3: Micro-Task Simulation (`test_simulate_api.py`)
- **Status:** HTTP 200 (Success)
- `GET /api/simulate/tasks` returned active simulation tasks.
- `POST /api/simulate` recorded submissions into `telos_sdc.simulation_results` with `evaluated: False` (ready for Person D on Day 4).

---

### 4. How to Re-Run the Checks

```powershell
# Test Priority 2 (Hybrid Search)
python src/test_match_api.py

# Test Priority 3 (Simulation endpoint)
python src/test_simulate_api.py
```
