"""Offline checks for the trusted-operator boundary; no external service calls."""

import os
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.testclient import TestClient

from backend.access import require_api_access
from backend.main import app


class ApiAccessTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_public_endpoints_remain_available(self):
        for path in ["/docs", "/health", "/openapi.json"]:
            self.assertEqual(self.client.get(path).status_code, 200)

    def test_missing_configuration_disables_data_access(self):
        with patch.dict(os.environ, {"API_ACCESS_TOKEN": ""}):
            self.assertEqual(self.client.get("/api/profiles").status_code, 503)

    def test_private_reads_reject_unauthenticated_callers(self):
        with patch.dict(os.environ, {"API_ACCESS_TOKEN": "offline-test-token"}):
            for path in [
                "/api/profiles",
                "/api/profile/example",
                "/api/match?user_id=example",
                "/api/simulate/history?user_id=example",
                "/api/simulate/tasks",
            ]:
                self.assertEqual(self.client.get(path).status_code, 401)
            self.assertEqual(
                self.client.get(
                    "/api/profiles", headers={"Authorization": "Bearer wrong"}
                ).status_code, 401
            )

    def test_writes_reject_unauthenticated_callers(self):
        with patch.dict(os.environ, {"API_ACCESS_TOKEN": "offline-test-token"}):
            for path in ["/api/profile", "/api/profile/upload", "/api/simulate"]:
                self.assertEqual(self.client.post(path, json={}).status_code, 401)

    def test_valid_operator_token_is_accepted(self):
        with patch.dict(os.environ, {"API_ACCESS_TOKEN": "offline-test-token"}):
            credentials = HTTPAuthorizationCredentials(
                scheme="Bearer", credentials="offline-test-token"
            )
            self.assertIsNone(require_api_access(credentials))
            with self.assertRaises(HTTPException) as error:
                require_api_access(None)
            self.assertEqual(error.exception.status_code, 401)


if __name__ == "__main__":
    unittest.main()
