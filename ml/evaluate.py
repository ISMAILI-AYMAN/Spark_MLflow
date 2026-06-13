"""Evaluate a trained churn model and print metrics."""

from __future__ import annotations

import json
from pathlib import Path

RESULTS = Path(__file__).parent / "results.json"


def main() -> None:
    if not RESULTS.exists():
        raise FileNotFoundError("Run ml/train_churn.py first.")

    data = json.loads(RESULTS.read_text(encoding="utf-8"))
    print(f"Best model: {data['best_model']} (CV AUC={data['best_cv_auc']})")
    for name, metrics in data.get("models", {}).items():
        print(f"\n{name}:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")


if __name__ == "__main__":
    main()
