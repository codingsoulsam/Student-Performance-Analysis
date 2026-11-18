import os
import json
import math

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE_PATH = os.path.join(BASE_DIR, "models", "model_bundle.json")

def load_bundle():
    with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def predict_single(data):
    # Extract Real Academic Inputs
    backlogs = int(data.get("backlogs", 0))
    attendance = float(data.get("attendance", 75))
    internals = float(data.get("internals", 60)) # in %
    prev_sgpa = float(data.get("prev_sgpa", 6.5)) # on scale 10
    study_hrs = float(data.get("study_hours", 2)) # hours/day
    assignments = data.get("assignments", "yes") # yes / no

    # 1. Backlogs Risk (0 -> 0%, 1 -> 40%, 2 -> 75%, 3+ -> 100%)
    if backlogs == 0:
        r_backlog = 0.0
    elif backlogs == 1:
        r_backlog = 45.0
    elif backlogs == 2:
        r_backlog = 80.0
    else:
        r_backlog = 100.0

    # 2. Attendance Risk (85%+ -> 0%, 75-84% -> 25%, 65-74% -> 65%, <65% -> 100%)
    if attendance >= 85:
        r_att = 5.0
    elif attendance >= 75:
        r_att = 25.0
    elif attendance >= 65:
        r_att = 70.0
    else:
        r_att = 98.0

    # 3. Internal Test Marks Risk (Out of 100%)
    if internals >= 75:
        r_internal = 5.0
    elif internals >= 50:
        r_internal = 30.0
    elif internals >= 40:
        r_internal = 65.0
    else:
        r_internal = 95.0

    # 4. Previous Semester SGPA Risk (scale 10)
    if prev_sgpa >= 7.5:
        r_sgpa = 5.0
    elif prev_sgpa >= 6.0:
        r_sgpa = 30.0
    elif prev_sgpa >= 5.0:
        r_sgpa = 65.0
    else:
        r_sgpa = 95.0

    # 5. Daily Study Hours Risk
    if study_hrs >= 3.0:
        r_study = 5.0
    elif study_hrs >= 1.5:
        r_study = 30.0
    else:
        r_study = 75.0

    # 6. Assignments Discipline
    r_assign = 10.0 if assignments == "yes" else 75.0

    # Weighted Composite Score
    total_risk = (
        (r_backlog * 0.35) +
        (r_att * 0.25) +
        (r_internal * 0.20) +
        (r_sgpa * 0.10) +
        (r_study * 0.06) +
        (r_assign * 0.04)
    )

    # Sigmoid smooth scaling for realistic bound
    total_risk = round(min(max(total_risk, 2.0), 98.5), 1)

    is_risk = total_risk >= 50.0

    return {
        "prediction": "At Risk" if is_risk else "Not At Risk",
        "risk_probability": total_risk,
        "breakdown": {
            "backlog_impact": round(r_backlog * 0.35, 1),
            "attendance_impact": round(r_att * 0.25, 1),
            "internal_impact": round(r_internal * 0.20, 1),
            "sgpa_impact": round(r_sgpa * 0.10, 1),
            "study_impact": round((r_study * 0.06) + (r_assign * 0.04), 1)
        },
        "student_metrics": {
            "attendance": attendance,
            "internals": internals,
            "prev_sgpa_pct": round(prev_sgpa * 10, 1),
            "study_pct": min(round((study_hrs / 4.0) * 100, 1), 100)
        }
    }
