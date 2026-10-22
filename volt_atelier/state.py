"""Interactive state for the schedule, plans, coaches, lab, and trial form."""

import reflex as rx

from volt_atelier.data import (
    BLANK_SESSION,
    CLASSES,
    COACHES,
    LANE_COLOR,
    PLAN_IDS,
    PLANS,
)
from volt_atelier.labmath import lab_result


def sessions_on(day: str, lane: str) -> list[dict[str, str]]:
    if lane == "All":
        return [item for item in CLASSES if item["day"] == day]
    return [item for item in CLASSES if item["day"] == day and item["type"] == lane]


class StudioState(rx.State):
    """One state object shared across the studio pages."""

    class_filter: str = "All"
    selected_class: str = ""
    yearly: bool = False
    chosen_plan: str = ""
    coach_id: str = "mara"
    units: str = "metric"
    sex: str = "female"
    age: str = "32"
    height: str = "168"
    weight: str = "64"
    activity: str = "moderate"
    goal: str = "maintain"
    trial_name: str = ""
    trial_email: str = ""
    trial_type: str = "Strength"
    trial_note: str = ""
    trial_error: str = ""
    trial_sent: bool = False
    open_faq: str = "trial"

    @rx.var
    def nav_path(self) -> str:
        path = self.router.url.path or "/"
        if not path.startswith("/"):
            path = "/" + path
        if len(path) > 1 and path.endswith("/"):
            path = path[:-1]
        return path

    @rx.var
    def sessions_mon(self) -> list[dict[str, str]]:
        return sessions_on("Mon", self.class_filter)

    @rx.var
    def sessions_tue(self) -> list[dict[str, str]]:
        return sessions_on("Tue", self.class_filter)

    @rx.var
    def sessions_wed(self) -> list[dict[str, str]]:
        return sessions_on("Wed", self.class_filter)

    @rx.var
    def sessions_thu(self) -> list[dict[str, str]]:
        return sessions_on("Thu", self.class_filter)

    @rx.var
    def sessions_fri(self) -> list[dict[str, str]]:
        return sessions_on("Fri", self.class_filter)

    @rx.var
    def sessions_sat(self) -> list[dict[str, str]]:
        return sessions_on("Sat", self.class_filter)

    @rx.var
    def sessions_sun(self) -> list[dict[str, str]]:
        return sessions_on("Sun", self.class_filter)

    @rx.var
    def board_label(self) -> str:
        lane = self.class_filter
        if lane == "All":
            count = len(CLASSES)
            return f"{count} sessions on this week's board"
        count = sum(item["type"] == lane for item in CLASSES)
        noun = "session" if count == 1 else "sessions"
        return f"{count} {lane} {noun}"

    @rx.var
    def has_selection(self) -> bool:
        key = self.selected_class
        return any(item["key"] == key for item in CLASSES)

    @rx.var
    def selected_session(self) -> dict[str, str]:
        key = self.selected_class
        for item in CLASSES:
            if item["key"] == key:
                return item
        return BLANK_SESSION

    @rx.var
    def chosen_label(self) -> str:
        for plan in PLANS:
            if plan["id"] == self.chosen_plan:
                return str(plan["name"])
        return ""

    @rx.var
    def active_coach(self) -> dict[str, str]:
        wanted = self.coach_id
        for coach in COACHES:
            if coach["id"] == wanted:
                return coach
        return COACHES[0]

    @rx.var
    def lab(self) -> dict[str, str]:
        return lab_result(
            units=self.units,
            sex=self.sex,
            age=self.age,
            height=self.height,
            weight=self.weight,
            activity=self.activity,
            goal=self.goal,
        )

    def set_trial_name(self, value: str):
        self.trial_name = value

    def set_trial_email(self, value: str):
        self.trial_email = value

    def set_trial_type(self, value: str):
        self.trial_type = value

    def set_trial_note(self, value: str):
        self.trial_note = value

    def set_age(self, value: str):
        self.age = value

    def set_height(self, value: str):
        self.height = value

    def set_weight(self, value: str):
        self.weight = value

    def set_sex(self, value: str):
        self.sex = value

    def set_activity(self, value: str):
        self.activity = value

    def set_goal(self, value: str):
        self.goal = value

    def sync_lane(self):
        raw = self.router.url.query_parameters.get("lane", "")
        if isinstance(raw, (list, tuple)):
            raw = raw[0] if raw else ""
        lane = str(raw or "")
        self.class_filter = lane if lane in LANE_COLOR else "All"
        self.selected_class = ""

    def set_class_filter(self, lane: str):
        if lane != "All" and lane not in LANE_COLOR:
            return
        self.class_filter = lane
        self.selected_class = ""

    def select_class(self, key: str):
        self.selected_class = "" if self.selected_class == key else key

    def clear_class(self):
        self.selected_class = ""

    def show_monthly(self):
        self.yearly = False

    def show_yearly(self):
        self.yearly = True

    def choose_plan(self, plan_id: str):
        if plan_id not in PLAN_IDS:
            return
        self.chosen_plan = plan_id
        return rx.scroll_to("trial")

    def select_coach(self, coach_id: str):
        if any(coach["id"] == coach_id for coach in COACHES):
            self.coach_id = coach_id

    def use_metric(self):
        if self.units == "metric":
            return
        height = _float_or_none(self.height)
        weight = _float_or_none(self.weight)
        if height is not None:
            self.height = f"{height * 2.54:.1f}"
        if weight is not None:
            self.weight = f"{weight * 0.45359237:.1f}"
        self.units = "metric"

    def use_imperial(self):
        if self.units == "imperial":
            return
        height = _float_or_none(self.height)
        weight = _float_or_none(self.weight)
        if height is not None:
            self.height = f"{height / 2.54:.1f}"
        if weight is not None:
            self.weight = f"{weight / 0.45359237:.1f}"
        self.units = "imperial"

    def reset_lab(self):
        self.units = "metric"
        self.sex = "female"
        self.age = "32"
        self.height = "168"
        self.weight = "64"
        self.activity = "moderate"
        self.goal = "maintain"

    def toggle_faq(self, key: str):
        self.open_faq = "" if self.open_faq == key else key

    def submit_trial(self):
        name = self.trial_name.strip()
        email = self.trial_email.strip()
        if len(name) < 2:
            self.trial_error = "Add the name that should go on the class sheet."
            self.trial_sent = False
            return
        domain = email.split("@")[-1] if "@" in email else ""
        if "@" not in email or "." not in domain or email.startswith("@") or " " in email:
            self.trial_error = "That email doesn't look ready to use."
            self.trial_sent = False
            return
        if self.trial_type not in LANE_COLOR:
            self.trial_error = "Pick a lane for the trial class."
            self.trial_sent = False
            return
        self.trial_name = name
        self.trial_email = email
        self.trial_note = self.trial_note.strip()
        self.trial_error = ""
        self.trial_sent = True

    def edit_trial(self):
        self.trial_sent = False
        self.trial_error = ""


def _float_or_none(raw: str) -> float | None:
    try:
        value = float(raw)
    except ValueError:
        return None
    return value
