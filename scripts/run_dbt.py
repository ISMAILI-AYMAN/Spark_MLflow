"""Run dbt via Docker (dbt incompatible with Python 3.14 locally)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DBT_CMD = os.getenv("DBT_DOCKER_CMD", "dbt")


def run_dbt(*args: str) -> None:
    network = os.getenv("DOCKER_NETWORK", "persoproject_default")
    cmd = [
        "docker",
        "run",
        "--rm",
        f"--network={network}",
        "-e",
        f"POSTGRES_HOST={os.getenv('POSTGRES_HOST', 'olist-postgres')}",
        "-e",
        f"POSTGRES_PORT={os.getenv('POSTGRES_PORT', '5432')}",
        "-e",
        f"POSTGRES_USER={os.getenv('POSTGRES_USER', 'olist')}",
        "-e",
        f"POSTGRES_PASSWORD={os.getenv('POSTGRES_PASSWORD', 'olist_secret')}",
        "-e",
        f"POSTGRES_DB={os.getenv('POSTGRES_DB', 'olist')}",
        "olist-dbt",
        *args,
        "--profiles-dir",
        ".",
    ]
    print(">>>", " ".join(cmd))
    subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)


def main() -> None:
    run_dbt(*sys.argv[1:] if len(sys.argv) > 1 else ["run"])


if __name__ == "__main__":
    main()
