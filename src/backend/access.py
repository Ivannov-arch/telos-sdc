"""Shared-token access for a trusted-operator development API."""

import os
import secrets

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer(auto_error=False)


def require_api_access(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer),
) -> None:
    expected = os.environ.get("API_ACCESS_TOKEN")
    if not expected:
        raise HTTPException(
            status_code=503,
            detail="Data API access is disabled until API_ACCESS_TOKEN is configured.",
        )
    if (
        credentials is None
        or credentials.scheme.lower() != "bearer"
        or not secrets.compare_digest(
            credentials.credentials.encode("utf-8"), expected.encode("utf-8")
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="A valid trusted-operator access token is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
