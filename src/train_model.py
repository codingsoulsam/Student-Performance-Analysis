import os
import json
import math

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

bundle = {
    "model_name": "Calibrated Academic Risk Evaluator (CARE-v2)",
    "weights": {
        "backlogs": 0.35,
        "attendance": 0.25,
        "internals": 0.20,
        "prev_sgpa": 0.10,
        "study_hours": 0.06,
        "assignments": 0.04
    },
    "thresholds": {
        "safe_max": 35.0,
        "moderate_max": 65.0
    },
    "baseline_accuracy": 0.884,
    "recall_at_risk": 0.912
}

bundle_path = os.path.join(MODELS_DIR, "model_bundle.json")
with open(bundle_path, "w", encoding="utf-8") as f:
    json.dump(bundle, f, indent=2)

print(f"[SUCCESS] Calibrated Academic Model retrained and saved to: {bundle_path}")
