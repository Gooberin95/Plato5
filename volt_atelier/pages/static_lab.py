"""BMI scale and calorie target, driven by one set of inputs."""

import reflex as rx

from volt_atelier.data import BLUE, GREEN, INK, LIME, ORANGE, YELLOW
from volt_atelier.frontend import (
    lab_activity,
    lab_age,
    lab_field,
    lab_goal,
    lab_height,
    lab_sex,
    lab_units,
    lab_weight,
    reset_lab,
    use_imperial,
    use_metric,
)
from volt_atelier.ui import (
    BODY,
    DISPLAY,
    FAINT,
    INK_DARK,
    LINE,
    MUTED,
    choice_row,
    field_label,
    glass,
    section_heading,
    shell,
    text_field,
)


def inputs() -> rx.Component:
    return glass(
        rx.el.h2(
            "Your numbers.",
            font_family=DISPLAY,
            font_weight="800",
            font_size="1.6rem",
            letter_spacing="-0.03em",
        ),
        rx.el.p(
            "The results update as you type. Switch units and the height and weight convert with you.",
            margin_top="0.4rem",
            color=MUTED,
            line_height="1.5",
        ),
        rx.vstack(
            rx.vstack(
                field_label("UNITS"),
                choice_row(
                    [("metric", "Metric"), ("imperial", "Imperial")],
                    lab_units.value,
                    _unit_setter,
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            rx.vstack(
                field_label("FORMULA CONSTANT"),
                choice_row(
                    [("female", "Female"), ("male", "Male")],
                    lab_sex.value,
                    lab_sex.set_value,
                ),
                rx.el.p(
                    "Calories use the two published Mifflin–St Jeor constants. BMI ignores this.",
                    color=FAINT,
                    font_size="0.82rem",
                    line_height="1.45",
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            rx.grid(
                rx.vstack(
                    field_label("AGE"),
                    text_field(lab_age.value, lab_age.set, "32"),
                    spacing="2",
                    width="100%",
                    align="start",
                ),
                rx.vstack(
                    field_label(rx.cond(lab_units.value == "metric", "HEIGHT (CM)", "HEIGHT (IN)")),
                    text_field(lab_height.value, lab_height.set, "168"),
                    spacing="2",
                    width="100%",
                    align="start",
                ),
                rx.vstack(
                    field_label(rx.cond(lab_units.value == "metric", "WEIGHT (KG)", "WEIGHT (LB)")),
                    text_field(lab_weight.value, lab_weight.set, "64"),
                    spacing="2",
                    width="100%",
                    align="start",
                ),
                columns=rx.breakpoints(initial="1", sm="3"),
                spacing="3",
                width="100%",
            ),
            rx.vstack(
                field_label("TRAINING WEEK"),
                choice_row(
                    [
                        ("sedentary", "Desk"),
                        ("light", "Light"),
                        ("moderate", "Moderate"),
                        ("hard", "Hard"),
                        ("athlete", "Athlete"),
                    ],
                    lab_activity.value,
                    lab_activity.set_value,
                ),
                rx.el.p(lab_field("activity_line"), color=MUTED, font_size="0.88rem"),
                spacing="2",
                align="start",
                width="100%",
            ),
            rx.vstack(
                field_label("AIM"),
                choice_row(
                    [("cut", "Cut"), ("maintain", "Maintain"), ("build", "Build")],
                    lab_goal.value,
                    lab_goal.set_value,
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            rx.el.button(
                "Reset the lab",
                type="button",
                on_click=reset_lab(),
                cursor="pointer",
                border_radius="999px",
                padding="0.55rem 0.9rem",
                font_weight="800",
                font_family=BODY,
                color=INK,
                background_color="transparent",
                border=f"1px solid {LINE}",
                align_self="flex-start",
            ),
            spacing="4",
            width="100%",
            margin_top="1rem",
            align="stretch",
        ),
        strong=True,
    )


def _unit_setter(value: str):
    if value == "imperial":
        return use_imperial()
    return use_metric()


def bmi_card() -> rx.Component:
    return glass(
        rx.el.p(
            "BODY MASS INDEX",
            color=LIME,
            font_size="0.72rem",
            font_weight="800",
            letter_spacing="0.14em",
        ),
        rx.el.p(
            lab_field("bmi"),
            margin_top="0.35rem",
            font_family=DISPLAY,
            font_weight="800",
            font_size="3.4rem",
            letter_spacing="-0.05em",
            line_height="0.9",
        ),
        rx.el.p(lab_field("category"), margin_top="0.45rem", font_weight="800"),
        rx.el.p(lab_field("bmi_detail"), margin_top="0.3rem", color=MUTED, line_height="1.5"),
        rx.box(
            rx.flex(
                rx.box(flex="14", height="12px", border_radius="999px", background_color=BLUE),
                rx.box(flex="26", height="12px", border_radius="999px", background_color=GREEN),
                rx.box(flex="20", height="12px", border_radius="999px", background_color=YELLOW),
                rx.box(flex="40", height="12px", border_radius="999px", background_color=ORANGE),
                width="100%",
                spacing="1",
                align="center",
            ),
            rx.cond(
                lab_field("ok") == "yes",
                rx.box(
                    position="absolute",
                    top="-6px",
                    left=lab_field("marker"),
                    width="4px",
                    height="24px",
                    border_radius="999px",
                    background_color=INK,
                    box_shadow=f"0 0 0 2px {INK_DARK}",
                    transform="translateX(-50%)",
                ),
                rx.box(),
            ),
            position="relative",
            width="100%",
            margin_top="1rem",
        ),
        rx.flex(
            rx.el.span("Under", flex="14", font_size="0.72rem", color=FAINT),
            rx.el.span("Steady", flex="26", font_size="0.72rem", color=FAINT),
            rx.el.span("Over", flex="20", font_size="0.72rem", color=FAINT),
            rx.el.span("High", flex="40", font_size="0.72rem", color=FAINT),
            width="100%",
            margin_top="0.4rem",
        ),
    )


def calorie_card() -> rx.Component:
    return glass(
        rx.el.p(
            "CALORIES",
            color=LIME,
            font_size="0.72rem",
            font_weight="800",
            letter_spacing="0.14em",
        ),
        rx.el.p(
            lab_field("sex_line"),
            " Mifflin–St Jeor, then the activity factor.",
            margin_top="0.35rem",
            color=FAINT,
            font_size="0.88rem",
        ),
        rx.grid(
            _metric("Basal", lab_field("bmr"), "kcal, before activity"),
            _metric("Burn", lab_field("tdee"), "kcal, your week"),
            _metric(lab_field("goal_label"), lab_field("target"), "kcal target"),
            columns=rx.breakpoints(initial="1", sm="3"),
            spacing="3",
            width="100%",
            margin_top="0.9rem",
        ),
        rx.box(
            rx.el.p(
                lab_field("protein"),
                " g protein",
                font_family=DISPLAY,
                font_weight="800",
                font_size="1.5rem",
                letter_spacing="-0.03em",
            ),
            rx.el.p(lab_field("protein_detail"), margin_top="0.3rem", color=MUTED, line_height="1.5"),
            margin_top="0.9rem",
        ),
        rx.cond(
            lab_field("ok") == "no",
            rx.el.p(lab_field("message"), margin_top="0.8rem", color="#ffb4c0", font_weight="700"),
            rx.box(),
        ),
    )


def _metric(label, value, note: str) -> rx.Component:
    return rx.box(
        rx.el.p(
            label,
            color=LIME,
            font_size="0.72rem",
            font_weight="800",
            letter_spacing="0.12em",
        ),
        rx.el.p(
            value,
            margin_top="0.25rem",
            font_family=DISPLAY,
            font_weight="800",
            font_size=rx.breakpoints(initial="1.7rem", md="2rem"),
            letter_spacing="-0.04em",
            line_height="1",
        ),
        rx.el.p(note, margin_top="0.3rem", color=FAINT, font_size="0.78rem"),
    )


def lab_page() -> rx.Component:
    return shell(
        rx.vstack(
            section_heading(
                "BODY LAB",
                "A number you can train with.",
                "BMI on one side, a calorie target on the other. Both are screening tools. Neither is a diagnosis, and neither is the workout.",
            ),
            rx.grid(
                inputs(),
                rx.vstack(bmi_card(), calorie_card(), spacing="3", width="100%"),
                columns=rx.breakpoints(initial="1", lg="2"),
                spacing="4",
                width="100%",
                align="start",
            ),
            glass(
                rx.el.p(
                    "The lab is educational. It is not medical advice, a meal plan, or a promise about what your body will do. If something hurts or a clinician has already given you numbers, use those.",
                    color=MUTED,
                    line_height="1.55",
                ),
                pad="1rem",
            ),
            spacing="4",
            width="100%",
            align="stretch",
        )
    )
