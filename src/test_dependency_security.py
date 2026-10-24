"""Offline regression checks for the backend's dependency security baseline."""

import importlib.metadata
from pathlib import Path
import tomllib
import unittest

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version


ROOT = Path(__file__).resolve().parents[1]
SECURITY_FLOORS = {
    "anyio": "4.14.2",
    "certifi": "2026.10.19",
    "idna": "3.15",
}
# These are separate distributions, not newer releases of httpx/httpcore.
# The backend and Supabase use the original httpx/httpcore packages.
UNUSED_FLAGGED_PACKAGES = {"httpx2", "httpcore2"}


class DependencySecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = tomllib.loads((ROOT / "pyproject.toml").read_text())
        cls.lock = tomllib.loads((ROOT / "uv.lock").read_text())

    def test_both_install_paths_enforce_security_floors(self):
        manifests = {
            "pyproject.toml": self.project["project"]["dependencies"],
            "requirements.txt": [
                line.strip()
                for line in (ROOT / "src/backend/requirements.txt").read_text().splitlines()
                if line.strip() and not line.lstrip().startswith("#")
            ],
        }
        for manifest, lines in manifests.items():
            requirements = {
                canonicalize_name(req.name): req
                for req in map(Requirement, lines)
            }
            for name, floor in SECURITY_FLOORS.items():
                with self.subTest(manifest=manifest, package=name):
                    self.assertIn(name, requirements)
                    # A newer lower bound is fine, but removing the security
                    # floor must fail even if today's lockfile remains safe.
                    lower_bounds = [
                        Version(spec.version)
                        for spec in requirements[name].specifier
                        if spec.operator in (">=", ">", "==") and "*" not in spec.version
                    ]
                    self.assertTrue(
                        any(bound >= Version(floor) for bound in lower_bounds),
                        f"{manifest} must require {name}>={floor}",
                    )

    def test_locked_and_installed_versions_are_patched(self):
        packages = {
            canonicalize_name(package["name"]): package
            for package in self.lock["package"]
        }
        for name, floor in SECURITY_FLOORS.items():
            with self.subTest(package=name):
                self.assertGreaterEqual(Version(packages[name]["version"]), Version(floor))
                self.assertGreaterEqual(
                    Version(importlib.metadata.version(name)), Version(floor)
                )

    def test_unused_flagged_http_packages_are_absent(self):
        locked = {
            canonicalize_name(package["name"]) for package in self.lock["package"]
        }
        installed = {
            canonicalize_name(dist.metadata["Name"])
            for dist in importlib.metadata.distributions()
        }
        self.assertTrue(UNUSED_FLAGGED_PACKAGES.isdisjoint(locked))
        self.assertTrue(UNUSED_FLAGGED_PACKAGES.isdisjoint(installed))
        self.assertTrue({"httpx", "httpcore"}.issubset(locked))
        self.assertTrue({"httpx", "httpcore"}.issubset(installed))


if __name__ == "__main__":
    unittest.main()
