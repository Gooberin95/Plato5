"""Browser state used only by the GitHub Pages build.

Pages cannot run the Reflex backend, so filters, forms, and the lab update
in ``useState``. ``reflex run`` and Azure do not import this module.
"""

import json

import reflex as rx
from reflex.experimental.client_state import ClientStateVar
from reflex_base.event import EventChain
from reflex_base.utils.imports import ImportVar
from reflex_base.vars import VarData
from reflex_base.vars.base import Var
from reflex_base.vars.function import FunctionVar

from volt_atelier.data import CLASSES, LANE_COLOR, PLANS

lane_filter = ClientStateVar.create("laneFilter", "All")
selected_class = ClientStateVar.create("selectedClass", "")
yearly = ClientStateVar.create("yearlyBilling", False)
chosen_plan = ClientStateVar.create("chosenPlan", "")
coach_id = ClientStateVar.create("coachId", "mara")
lab_units = ClientStateVar.create("labUnits", "metric")
lab_sex = ClientStateVar.create("labSex", "female")
lab_age = ClientStateVar.create("labAge", "32")
lab_height = ClientStateVar.create("labHeight", "168")
lab_weight = ClientStateVar.create("labWeight", "64")
lab_activity = ClientStateVar.create("labActivity", "moderate")
lab_goal = ClientStateVar.create("labGoal", "maintain")
trial_name = ClientStateVar.create("trialName", "")
trial_email = ClientStateVar.create("trialEmail", "")
trial_type = ClientStateVar.create("trialType", "Strength")
trial_note = ClientStateVar.create("trialNote", "")
trial_error = ClientStateVar.create("trialError", "")
trial_sent = ClientStateVar.create("trialSent", False)
open_faq = ClientStateVar.create("openFaq", "trial")

CLIENT_VARS = (
    lane_filter,
    selected_class,
    yearly,
    chosen_plan,
    coach_id,
    lab_units,
    lab_sex,
    lab_age,
    lab_height,
    lab_weight,
    lab_activity,
    lab_goal,
    trial_name,
    trial_email,
    trial_type,
    trial_note,
    trial_error,
    trial_sent,
    open_faq,
)

LANES = list(LANE_COLOR)
_LANE_JS = json.dumps(LANES)


def _get(var: ClientStateVar) -> str:
    return f"refs['_client_state_{var._getter_name}']"


def _set(var: ClientStateVar) -> str:
    return f"refs['_client_state_{var._setter_name}']"


def _data(*deps: ClientStateVar, hooks: dict | None = None, imports: dict | None = None) -> VarData | None:
    extra = []
    if hooks or imports:
        extra.append(VarData(hooks=hooks, imports=imports))
    return VarData.merge(*(dep._var_data for dep in deps), *extra)


def client_expr(expression: str, *deps: ClientStateVar, hooks: dict | None = None, imports: dict | None = None) -> Var:
    return Var(
        _js_expr=expression,
        _var_data=_data(*deps, hooks=hooks, imports=imports),
    )


def client_action(body: str, *deps: ClientStateVar) -> EventChain:
    return client_expr(f"() => {{ {body} }}", *deps).to(FunctionVar, EventChain)


def path_is(href: str) -> Var:
    expression = (
        "(() => {"
        "const raw = (__navLoc.pathname || '/');"
        "const trimmed = raw.length > 1 && raw.endsWith('/') ? raw.slice(0, -1) : raw;"
        "const base = '/Plato5';"
        "const path = trimmed === base ? '/' : (trimmed.startsWith(base + '/') ? trimmed.slice(base.length) : trimmed);"
        f"return path === {json.dumps(href)};"
        "})()"
    )
    return Var(
        _js_expr=expression,
        _var_data=VarData(
            imports={"react-router": [ImportVar(tag="useLocation")]},
            hooks={"const __navLoc = useLocation()": None},
        ),
    )


def set_lane(name: str):
    return client_action(
        f"{_set(lane_filter)}({json.dumps(name)}); {_set(selected_class)}('');",
        lane_filter,
        selected_class,
    )


def toggle_class(key: str):
    return client_action(
        f"{_set(selected_class)}({_get(selected_class)} === {json.dumps(key)} ? '' : {json.dumps(key)});",
        selected_class,
    )


def clear_class():
    return client_action(f"{_set(selected_class)}('');", selected_class)


def show_monthly():
    return yearly.set_value(False)


def show_yearly():
    return yearly.set_value(True)


def choose_plan(plan_id: str):
    return client_action(
        f"{_set(chosen_plan)}({json.dumps(plan_id)});"
        "const trial = document.getElementById('trial');"
        "if (trial) trial.scrollIntoView({behavior: 'smooth', block: 'start'});",
        chosen_plan,
    )


def select_coach(coach: str):
    return coach_id.set_value(coach)


def toggle_faq(key: str):
    return client_action(
        f"{_set(open_faq)}({_get(open_faq)} === {json.dumps(key)} ? '' : {json.dumps(key)});",
        open_faq,
    )


def _convert_units(to_metric: bool) -> EventChain:
    height = _get(lab_height)
    weight = _get(lab_weight)
    units = _get(lab_units)
    if to_metric:
        height_factor = "* 2.54"
        weight_factor = "* 0.45359237"
        target = "metric"
        guard = f"{units} === 'metric'"
    else:
        height_factor = "/ 2.54"
        weight_factor = "/ 0.45359237"
        target = "imperial"
        guard = f"{units} === 'imperial'"
    body = f"""
        if ({guard}) return;
        const height = parseFloat(String({height} ?? '').trim());
        const weight = parseFloat(String({weight} ?? '').trim());
        if (Number.isFinite(height)) {_set(lab_height)}((height {height_factor}).toFixed(1));
        if (Number.isFinite(weight)) {_set(lab_weight)}((weight {weight_factor}).toFixed(1));
        {_set(lab_units)}({json.dumps(target)});
    """
    return client_action(body, lab_units, lab_height, lab_weight)


def use_metric():
    return _convert_units(True)


def use_imperial():
    return _convert_units(False)


def reset_lab():
    return client_action(
        f"""
        {_set(lab_units)}('metric');
        {_set(lab_sex)}('female');
        {_set(lab_age)}('32');
        {_set(lab_height)}('168');
        {_set(lab_weight)}('64');
        {_set(lab_activity)}('moderate');
        {_set(lab_goal)}('maintain');
        """,
        lab_units,
        lab_sex,
        lab_age,
        lab_height,
        lab_weight,
        lab_activity,
        lab_goal,
    )


def submit_trial():
    body = f"""
        const name = String({_get(trial_name)} ?? '').trim();
        const email = String({_get(trial_email)} ?? '').trim();
        const note = String({_get(trial_note)} ?? '').trim();
        const type = String({_get(trial_type)} ?? '');
        const domain = email.includes('@') ? email.split('@').slice(1).join('@') : '';
        if (name.length < 2) {{
            {_set(trial_error)}('Add the name that should go on the class sheet.');
            {_set(trial_sent)}(false);
            return;
        }}
        if (!email.includes('@') || !domain.includes('.') || email.startsWith('@') || email.includes(' ')) {{
            {_set(trial_error)}("That email doesn't look ready to use.");
            {_set(trial_sent)}(false);
            return;
        }}
        if (!{_LANE_JS}.includes(type)) {{
            {_set(trial_error)}('Pick a lane for the trial class.');
            {_set(trial_sent)}(false);
            return;
        }}
        {_set(trial_name)}(name);
        {_set(trial_email)}(email);
        {_set(trial_note)}(note);
        {_set(trial_error)}('');
        {_set(trial_sent)}(true);
    """
    return client_action(
        body,
        trial_name,
        trial_email,
        trial_note,
        trial_type,
        trial_error,
        trial_sent,
    )


def edit_trial():
    return client_action(
        f"{_set(trial_sent)}(false); {_set(trial_error)}('');",
        trial_sent,
        trial_error,
    )


def board_label() -> Var:
    counts = {name: 0 for name in LANE_COLOR}
    for item in CLASSES:
        counts[item["type"]] += 1
    labels = {"All": f"{len(CLASSES)} sessions on this week's board"}
    for name, count in counts.items():
        noun = "session" if count == 1 else "sessions"
        labels[name] = f"{count} {name} {noun}"
    return client_expr(f"({json.dumps(labels)}[{_get(lane_filter)}] || '')", lane_filter)


def lane_is(name: str) -> Var:
    if name == "All":
        return lane_filter.value == "All"
    return (lane_filter.value == "All") | (lane_filter.value == name)


def day_is_empty(day: str) -> Var:
    sessions = [item for item in CLASSES if item["day"] == day]
    if not sessions:
        return client_expr("true", lane_filter)
    checks = " && ".join(
        f"({_get(lane_filter)} !== 'All' && {_get(lane_filter)} !== {json.dumps(item['type'])})"
        for item in sessions
    )
    return client_expr(f"({checks})", lane_filter)


def chosen_name() -> Var:
    labels = {plan["id"]: plan["name"] for plan in PLANS}
    return client_expr(f"({json.dumps(labels)}[{_get(chosen_plan)}] || '')", chosen_plan)


def lane_sync() -> rx.Component:
    effect = f"""
        useEffect(() => {{
            const path = (__laneLoc.pathname || '').replace(/\\/+$/, '') || '/';
            if (!path.endsWith('/schedule')) return;
            const lane = new URLSearchParams(__laneLoc.search).get('lane') || '';
            const allowed = {_LANE_JS};
            {_set(lane_filter)}(allowed.includes(lane) ? lane : 'All');
            {_set(selected_class)}('');
        }}, [__laneLoc.pathname, __laneLoc.search])
    """
    marker = Var(
        _js_expr="null",
        _var_data=_data(
            lane_filter,
            selected_class,
            hooks={
                "const __laneLoc = useLocation()": None,
                effect: None,
            },
            imports={
                "react": [ImportVar(tag="useEffect")],
                "react-router": [ImportVar(tag="useLocation")],
            },
        ),
    )
    return rx.box(marker, display="none")


_LAB_HOOK = """
const voltLab = (() => {
    const read = (name) => refs['_client_state_' + name];
    const num = (raw) => {
        const value = parseFloat(String(raw ?? '').trim());
        return Number.isFinite(value) ? value : null;
    };
    const grouped = (value) => Math.round(value).toLocaleString('en-US');
    const activityTable = {
        sedentary: [1.2, 'Desk day, little training'],
        light: [1.375, 'One or two easy sessions'],
        moderate: [1.55, 'Three to five sessions'],
        hard: [1.725, 'Six days, some of them long'],
        athlete: [1.9, 'Physical work plus training'],
    };
    const goalTable = {
        cut: [0.85, 'Cut', 2.0, "A modest deficit. Don't stack extra cardio on top of Kiln days."],
        maintain: [1.0, 'Maintain', 1.6, 'Hold here most weeks. Eat a little more after the long rides.'],
        build: [1.1, 'Build', 1.8, 'A small surplus for the barbell. A huge one just makes Restore harder.'],
    };
    const units = String(read('labUnits') || 'metric');
    const sex = String(read('labSex') || 'female');
    const activityKey = activityTable[read('labActivity')] ? read('labActivity') : 'moderate';
    const goalKey = goalTable[read('labGoal')] ? read('labGoal') : 'maintain';
    const factor = activityTable[activityKey][0];
    const activityLine = activityTable[activityKey][1];
    const multiplier = goalTable[goalKey][0];
    const goalLabel = goalTable[goalKey][1];
    const proteinPerKg = goalTable[goalKey][2];
    const proteinDetail = goalTable[goalKey][3];
    const blank = {
        ok: 'no',
        message: '',
        bmi: '\\u2014',
        category: 'Waiting on numbers',
        bmi_detail: 'BMI uses height and weight only.',
        marker: '0%',
        bmr: '\\u2014',
        tdee: '\\u2014',
        target: '\\u2014',
        goal_label: goalLabel,
        protein: '\\u2014',
        protein_detail: proteinDetail,
        sex_line: '',
        activity_line: activityLine,
    };
    const age = num(read('labAge'));
    const heightRaw = num(read('labHeight'));
    const weightRaw = num(read('labWeight'));
    if (age === null || heightRaw === null || weightRaw === null) {
        blank.message = 'Enter a number for age, height, and weight.';
        return blank;
    }
    if (age < 16) {
        blank.message = 'Volt Atelier trains adults. The lab starts at 16.';
        return blank;
    }
    if (age > 90) {
        blank.message = 'Use an age of 90 or under.';
        return blank;
    }
    if (sex !== 'female' && sex !== 'male') {
        blank.message = 'Pick a formula constant.';
        return blank;
    }
    let heightCm = heightRaw;
    let weightKg = weightRaw;
    if (units === 'imperial') {
        if (heightRaw < 48 || heightRaw > 90) {
            blank.message = 'Enter a height between 48 and 90 inches.';
            return blank;
        }
        if (weightRaw < 80 || weightRaw > 550) {
            blank.message = 'Enter a weight between 80 and 550 pounds.';
            return blank;
        }
        heightCm = heightRaw * 2.54;
        weightKg = weightRaw * 0.45359237;
    } else {
        if (heightRaw < 120 || heightRaw > 230) {
            blank.message = 'Enter a height between 120 and 230 cm.';
            return blank;
        }
        if (weightRaw < 35 || weightRaw > 250) {
            blank.message = 'Enter a weight between 35 and 250 kg.';
            return blank;
        }
    }
    const bmi = weightKg / ((heightCm / 100) ** 2);
    let category = 'Well above the reference range';
    let detail = '30 or higher. Still just a screening number.';
    if (bmi < 18.5) {
        category = 'Under the reference range';
        detail = 'Below 18.5. Useful context, not a verdict.';
    } else if (bmi < 25) {
        category = 'Inside the reference range';
        detail = '18.5 to 24.9. A screening band, not a goal by itself.';
    } else if (bmi < 30) {
        category = 'Above the reference range';
        detail = '25 to 29.9. Coaches look at the work, not this number alone.';
    }
    let bmr = 10 * weightKg + 6.25 * heightCm - 5 * age;
    bmr += sex === 'male' ? 5 : -161;
    const tdee = bmr * factor;
    const target = tdee * multiplier;
    const protein = weightKg * proteinPerKg;
    const marker = Math.max(0, Math.min(100, ((bmi - 15) / 25) * 100));
    return {
        ok: 'yes',
        message: '',
        bmi: bmi.toFixed(1),
        category,
        bmi_detail: detail,
        marker: marker.toFixed(1) + '%',
        bmr: grouped(bmr),
        tdee: grouped(tdee),
        target: grouped(target),
        goal_label: goalLabel,
        protein: String(Math.round(protein)),
        protein_detail: proteinDetail,
        sex_line: sex === 'male' ? 'Male constant, +5 kcal.' : 'Female constant, \\u2212161 kcal.',
        activity_line: activityLine,
    };
})()
"""

_LAB_DEPS = (lab_units, lab_sex, lab_age, lab_height, lab_weight, lab_activity, lab_goal)


def lab_field(key: str) -> Var:
    return client_expr(
        f"voltLab[{json.dumps(key)}]",
        *_LAB_DEPS,
        hooks={_LAB_HOOK: None},
    )
