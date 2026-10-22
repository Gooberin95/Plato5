"""Pure BMI and calorie math for the Body Lab.

The calorie target uses the Mifflin–St Jeor equation times an activity factor.
"""

from __future__ import annotations

import math

ACTIVITY: dict[str, tuple[float, str]] = {
    "sedentary": (1.2, "Desk day, little training"),
    "light": (1.375, "One or two easy sessions"),
    "moderate": (1.55, "Three to five sessions"),
    "hard": (1.725, "Six days, some of them long"),
    "athlete": (1.9, "Physical work plus training"),
}

GOAL: dict[str, tuple[float, str, float, str]] = {
    "cut": (
        0.85,
        "Cut",
        2.0,
        "A modest deficit. Don't stack extra cardio on top of Kiln days.",
    ),
    "maintain": (
        1.0,
        "Maintain",
        1.6,
        "Hold here most weeks. Eat a little more after the long rides.",
    ),
    "build": (
        1.1,
        "Build",
        1.8,
        "A small surplus for the barbell. A huge one just makes Restore harder.",
    ),
}

_BLANK: dict[str, str] = {
    "ok": "no",
    "message": "",
    "bmi": "—",
    "category": "Waiting on numbers",
    "bmi_detail": "BMI uses height and weight only.",
    "marker": "0%",
    "bmr": "—",
    "tdee": "—",
    "target": "—",
    "goal_label": "Maintain",
    "protein": "—",
    "protein_detail": "",
    "sex_line": "",
    "activity_line": "",
}


def _number(raw: str) -> float | None:
    try:
        value = float(str(raw).strip())
    except ValueError:
        return None
    if not math.isfinite(value):
        return None
    return value


def lab_result(
    *,
    units: str,
    sex: str,
    age: str,
    height: str,
    weight: str,
    activity: str,
    goal: str,
) -> dict[str, str]:
    """Return display strings for the BMI scale and the calorie target."""
    activity_key = activity if activity in ACTIVITY else "moderate"
    goal_key = goal if goal in GOAL else "maintain"
    factor, activity_line = ACTIVITY[activity_key]
    multiplier, goal_label, protein_per_kg, protein_detail = GOAL[goal_key]

    result = dict(_BLANK)
    result["activity_line"] = activity_line
    result["goal_label"] = goal_label
    result["protein_detail"] = protein_detail

    age_value = _number(age)
    height_value = _number(height)
    weight_value = _number(weight)
    if age_value is None or height_value is None or weight_value is None:
        result["message"] = "Enter a number for age, height, and weight."
        return result
    if age_value < 16:
        result["message"] = "Volt Atelier trains adults. The lab starts at 16."
        return result
    if age_value > 90:
        result["message"] = "Use an age of 90 or under."
        return result
    if sex not in ("female", "male"):
        result["message"] = "Pick a formula constant."
        return result

    if units == "imperial":
        if not 48 <= height_value <= 90:
            result["message"] = "Enter a height between 48 and 90 inches."
            return result
        if not 80 <= weight_value <= 550:
            result["message"] = "Enter a weight between 80 and 550 pounds."
            return result
        height_cm = height_value * 2.54
        weight_kg = weight_value * 0.45359237
    else:
        if not 120 <= height_value <= 230:
            result["message"] = "Enter a height between 120 and 230 cm."
            return result
        if not 35 <= weight_value <= 250:
            result["message"] = "Enter a weight between 35 and 250 kg."
            return result
        height_cm = height_value
        weight_kg = weight_value

    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:
        category = "Under the reference range"
        detail = "Below 18.5. Useful context, not a verdict."
    elif bmi < 25:
        category = "Inside the reference range"
        detail = "18.5 to 24.9. A screening band, not a goal by itself."
    elif bmi < 30:
        category = "Above the reference range"
        detail = "25 to 29.9. Coaches look at the work, not this number alone."
    else:
        category = "Well above the reference range"
        detail = "30 or higher. Still just a screening number."

    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age_value
    bmr += 5 if sex == "male" else -161
    tdee = bmr * factor
    target = tdee * multiplier
    protein = weight_kg * protein_per_kg
    marker = max(0.0, min(100.0, (bmi - 15) / 25 * 100))

    result.update(
        {
            "ok": "yes",
            "message": "",
            "bmi": f"{bmi:.1f}",
            "category": category,
            "bmi_detail": detail,
            "marker": f"{marker:.1f}%",
            "bmr": f"{bmr:,.0f}",
            "tdee": f"{tdee:,.0f}",
            "target": f"{target:,.0f}",
            "protein": f"{protein:.0f}",
            "sex_line": (
                "Male constant, +5 kcal."
                if sex == "male"
                else "Female constant, −161 kcal."
            ),
        }
    )
    return result
