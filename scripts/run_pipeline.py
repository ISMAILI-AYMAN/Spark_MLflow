"""Run full pipeline locally: bronze load -> dbt -> churn training."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"\n>>> {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd or PROJECT_ROOT, check=True)


def main() -> None:
    sys.path.insert(0, str(PROJECT_ROOT))
    from ingestion.load_bronze import main as load_bronze

    load_bronze()

    dbt_dir = PROJECT_ROOT / "dbt"
    run(["python", str(PROJECT_ROOT / "scripts" / "run_dbt.py"), "run"])
    run(["python", str(PROJECT_ROOT / "scripts" / "run_dbt.py"), "test"])

    from ml.train_churn import main as train_churn

    train_churn()
    print("\nPipeline complete.")
    print("Optional: python scripts/export_powerbi_csvs.py")


if __name__ == "__main__":
    main()
