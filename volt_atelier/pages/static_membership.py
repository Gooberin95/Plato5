"""Membership tiers, monthly/yearly billing, and the trial request."""

import reflex as rx

from volt_atelier.data import FAQS, LANE_COLOR, LIME, PLANS
from volt_atelier.frontend import (
    choose_plan,
    chosen_name,
    chosen_plan,
    edit_trial,
    open_faq,
    submit_trial,
    toggle_faq,
    trial_email,
    trial_error,
    trial_name,
    trial_note,
    trial_sent,
    trial_type,
    yearly,
)
from volt_atelier.ui import (
    BODY,
    DISPLAY,
    FAINT,
    GLASS,
    INK,
    INK_DARK,
    LINE,
    MUTED,
    billing_toggle,
    choice_row,
    field_label,
    glass,
    price_figure,
    section_heading,
    shell,
    text_field,
)


def plan_card(plan: dict) -> rx.Component:
    chosen = chosen_plan.value == plan["id"]
    border = f"1px solid {LIME}" if plan["featured"] else f"1px solid {LINE}"
    return glass(
        (
            rx.el.span(
                "MOST CHOSEN",
                display="inline-flex",
                border_radius="999px",
                padding="0.18rem 0.55rem",
                background_color=LIME,
                color=INK_DARK,
                font_size="0.68rem",
                font_weight="800",
                letter_spacing="0.08em",
            )
            if plan["featured"]
            else rx.box()
        ),
        rx.el.h3(
            plan["name"],
            margin_top="0.7rem",
            font_family=DISPLAY,
            font_weight="800",
            font_size="2rem",
            letter_spacing="-0.04em",
        ),
        rx.el.p(plan["kicker"], color=LIME, font_weight="800", margin_top="0.15rem"),
        rx.el.p(plan["blurb"], margin_top="0.45rem", color=MUTED, line_height="1.5"),
        rx.box(
            price_figure(plan["monthly"], plan["yearly_month"]),
            margin_top="0.9rem",
        ),
        rx.cond(
            yearly.value,
            rx.el.p(
                f"Save ${plan['save']} against paying monthly. Billed ${plan['yearly_total']} for the year.",
                margin_top="0.55rem",
                color=MUTED,
                font_size="0.9rem",
                line_height="1.45",
            ),
            rx.el.p(
                "Billed each month. Leave when you want.",
                margin_top="0.55rem",
                color=FAINT,
                font_size="0.9rem",
            ),
        ),
        rx.vstack(
            *[
                rx.flex(
                    rx.box(
                        width="8px",
                        height="8px",
                        border_radius="999px",
                        background_color=LIME,
                        flex_shrink="0",
                        margin_top="0.4rem",
                    ),
                    rx.el.span(feature, line_height="1.4"),
                    spacing="2",
                    align="start",
                    width="100%",
                )
                for feature in plan["features"]
            ],
            spacing="2",
            width="100%",
            margin_top="1rem",
            align="start",
        ),
        rx.el.button(
            rx.cond(chosen, "Chosen for the trial", f"Choose {plan['name']}"),
            type="button",
            on_click=choose_plan(plan["id"]),
            cursor="pointer",
            width="100%",
            margin_top="1.1rem",
            border_radius="999px",
            padding="0.8rem 1rem",
            font_weight="800",
            font_family=BODY,
            background_color=rx.cond(chosen, LIME, "transparent"),
            color=rx.cond(chosen, INK_DARK, INK),
            border=rx.cond(chosen, "1px solid transparent", f"1px solid {LINE}"),
        ),
        border=border,
        strong=plan["featured"],
    )


def faq_list() -> rx.Component:
    return glass(
        rx.el.h2(
            "Before you ask the desk.",
            font_family=DISPLAY,
            font_weight="800",
            font_size="1.7rem",
            letter_spacing="-0.03em",
        ),
        *[faq_item(key, question, answer) for key, question, answer in FAQS],
        strong=True,
        margin_top="0.4rem",
    )


def faq_item(key: str, question: str, answer: str) -> rx.Component:
    opened = open_faq.value == key
    return rx.box(
        rx.el.button(
            rx.flex(
                rx.el.span(question, font_weight="800", text_align="left"),
                rx.el.span(
                    rx.cond(opened, "–", "+"),
                    color=LIME,
                    font_family=DISPLAY,
                    font_size="1.3rem",
                    flex_shrink="0",
                ),
                justify="between",
                align="center",
                width="100%",
                spacing="3",
            ),
            type="button",
            on_click=toggle_faq(key),
            width="100%",
            cursor="pointer",
            background_color="transparent",
            color=INK,
            padding="0.95rem 0",
            text_align="left",
            font_family=BODY,
            font_size="1rem",
        ),
        rx.cond(
            opened,
            rx.el.p(
                answer,
                color=MUTED,
                line_height="1.6",
                padding_bottom="0.95rem",
            ),
        ),
        border_bottom=f"1px solid {LINE}",
        width="100%",
    )


def trial_form() -> rx.Component:
    lanes = [(lane, lane) for lane in LANE_COLOR]
    return rx.box(
        glass(
            rx.el.h2(
                "Book the free class.",
                font_family=DISPLAY,
                font_weight="800",
                font_size=rx.breakpoints(initial="1.8rem", md="2.3rem"),
                letter_spacing="-0.03em",
            ),
            rx.el.p(
                "Tell the desk your name, a real email shape, and the lane you want to try. Nothing is charged. This demo keeps the request in the session only.",
                margin_top="0.55rem",
                color=MUTED,
                line_height="1.55",
                max_width="40rem",
            ),
            rx.cond(
                chosen_plan.value != "",
                rx.el.p(
                    "Plan held for this session: ",
                    chosen_name(),
                    ". We'll mention it with the request.",
                    margin_top="0.7rem",
                    color=LIME,
                    font_weight="700",
                ),
                rx.box(),
            ),
            rx.cond(
                trial_sent.value,
                trial_success(),
                rx.vstack(
                    rx.grid(
                        rx.vstack(
                            field_label("NAME"),
                            text_field(trial_name.value, trial_name.set, "Priya D."),
                            spacing="2",
                            align="start",
                            width="100%",
                        ),
                        rx.vstack(
                            field_label("EMAIL"),
                            text_field(
                                trial_email.value,
                                trial_email.set,
                                "you@domain.com",
                            ),
                            spacing="2",
                            align="start",
                            width="100%",
                        ),
                        columns=rx.breakpoints(initial="1", sm="2"),
                        spacing="3",
                        width="100%",
                    ),
                    rx.vstack(
                        field_label("LANE"),
                        choice_row(lanes, trial_type.value, trial_type.set_value),
                        spacing="2",
                        align="start",
                        width="100%",
                    ),
                    rx.vstack(
                        field_label("NOTE"),
                        rx.text_area(
                            value=trial_note.value,
                            on_change=trial_note.set,
                            placeholder="New to a barbell, or chasing a ride PR. Optional.",
                            width="100%",
                            size="3",
                            variant="soft",
                            color_scheme="gray",
                            radius="large",
                            resize="vertical",
                        ),
                        spacing="2",
                        align="start",
                        width="100%",
                    ),
                    rx.cond(
                        trial_error.value != "",
                        rx.el.p(trial_error.value, color="#ffb4c0", font_weight="700"),
                        rx.box(),
                    ),
                    rx.el.button(
                        "Request the trial",
                        type="button",
                        on_click=submit_trial(),
                        cursor="pointer",
                        border_radius="999px",
                        padding="0.85rem 1.2rem",
                        font_weight="800",
                        font_family=BODY,
                        background_color=LIME,
                        color=INK_DARK,
                        border="1px solid transparent",
                        align_self="flex-start",
                    ),
                    spacing="4",
                    width="100%",
                    margin_top="1rem",
                    align="stretch",
                ),
            ),
            strong=True,
        ),
        id="trial",
        scroll_margin_top="5.8rem",
    )


def trial_success() -> rx.Component:
    return rx.box(
        rx.el.p(
            "You're on the sheet.",
            margin_top="1rem",
            font_family=DISPLAY,
            font_weight="800",
            font_size="1.8rem",
            letter_spacing="-0.03em",
        ),
        rx.el.p(
            trial_name.value,
            " · ",
            trial_email.value,
            " · ",
            trial_type.value,
            margin_top="0.55rem",
            color=MUTED,
        ),
        rx.cond(
            chosen_plan.value != "",
            rx.el.p(
                "Plan noted: ",
                chosen_name(),
                ".",
                margin_top="0.35rem",
                color=LIME,
                font_weight="700",
            ),
            rx.box(),
        ),
        rx.cond(
            trial_note.value != "",
            rx.el.p(
                trial_note.value,
                margin_top="0.55rem",
                color=MUTED,
                line_height="1.5",
            ),
            rx.box(),
        ),
        rx.el.p(
            "Held in this browser session only. Refreshing or closing the tab clears it. Nobody was emailed.",
            margin_top="0.7rem",
            color=FAINT,
            font_size="0.9rem",
            line_height="1.5",
        ),
        rx.el.button(
            "Edit the request",
            type="button",
            on_click=edit_trial(),
            cursor="pointer",
            margin_top="0.9rem",
            border_radius="999px",
            padding="0.6rem 0.95rem",
            font_weight="800",
            font_family=BODY,
            color=INK,
            background_color="transparent",
            border=f"1px solid {LINE}",
        ),
        padding="0.4rem",
        border_radius="16px",
        background_color=GLASS,
    )


def membership_page() -> rx.Component:
    return shell(
        rx.vstack(
            section_heading(
                "MEMBERSHIP",
                "Three plans. No lobby pitch.",
                "Month to month, or a year at a lower rate. The yearly price is the monthly equivalent. The bill for the year is written on the card.",
            ),
            billing_toggle(),
            rx.grid(
                *[plan_card(plan) for plan in PLANS],
                columns=rx.breakpoints(initial="1", lg="3"),
                spacing="4",
                width="100%",
                align="stretch",
            ),
            rx.el.p(
                "Not ready to join? A day pass is $32 at the desk. Your first class is free either way.",
                color=MUTED,
            ),
            faq_list(),
            trial_form(),
            spacing="5",
            width="100%",
            align="stretch",
        )
    )
