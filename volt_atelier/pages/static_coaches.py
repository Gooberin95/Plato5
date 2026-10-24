"""Coach profiles. Selecting a card fills the detail panel."""

import reflex as rx

from volt_atelier.data import COACHES
from volt_atelier.frontend import coach_id, select_coach
from volt_atelier.ui import (
    BODY,
    DISPLAY,
    FAINT,
    INK,
    LINE,
    MUTED,
    glass,
    section_heading,
    shell,
)


def monogram(letters, accent, ink, size: str = "64px") -> rx.Component:
    return rx.flex(
        rx.el.span(
            letters,
            font_family=DISPLAY,
            font_weight="800",
            color=ink,
            font_size="1.15rem",
        ),
        width=size,
        height=size,
        border_radius="18px",
        background_color=accent,
        align="center",
        justify="center",
        flex_shrink="0",
    )


def detail() -> rx.Component:
    panels = []
    for coach in COACHES:
        panels.append(
            rx.cond(
                coach_id.value == coach["id"],
                glass(
                    rx.flex(
            monogram(coach["letters"], coach["accent"], coach["ink"], "84px"),
            rx.box(
                rx.el.p(
                    coach["role"],
                    color=coach["accent"],
                    font_size="0.75rem",
                    font_weight="800",
                    letter_spacing="0.14em",
                ),
                rx.el.h2(
                    coach["name"],
                    margin_top="0.2rem",
                    font_family=DISPLAY,
                    font_weight="800",
                    font_size=rx.breakpoints(initial="2rem", md="2.7rem"),
                    letter_spacing="-0.04em",
                    line_height="0.95",
                ),
                rx.el.p(
                    "“",
                    coach["quote"],
                    "”",
                    margin_top="0.7rem",
                    font_size="1.15rem",
                    line_height="1.45",
                ),
                rx.el.p(
                    coach["bio"],
                    margin_top="0.7rem",
                    color=MUTED,
                    line_height="1.6",
                ),
                rx.flex(
                    _meta(coach["years"]),
                    _meta(coach["focus"]),
                    rx.el.span(
                        "Signature · ",
                        coach["signature"],
                        border_radius="999px",
                        padding="0.3rem 0.65rem",
                        border=f"1px solid {LINE}",
                        color=MUTED,
                        font_size="0.82rem",
                        font_weight="700",
                    ),
                    spacing="2",
                    wrap="wrap",
                    margin_top="0.9rem",
                ),
                flex="1",
            ),
            direction=rx.breakpoints(initial="column", sm="row"),
            spacing="4",
            width="100%",
            align="start",
        ),
                    strong=True,
                ),
                rx.fragment(),
            )
        )
    return rx.box(*panels, width="100%")


def _meta(text) -> rx.Component:
    return rx.el.span(
        text,
        border_radius="999px",
        padding="0.3rem 0.65rem",
        border=f"1px solid {LINE}",
        color=MUTED,
        font_size="0.82rem",
        font_weight="700",
    )


def coach_card(coach: dict) -> rx.Component:
    active = coach_id.value == coach["id"]
    return rx.el.button(
        rx.flex(
            monogram(coach["letters"], coach["accent"], coach["ink"]),
            rx.box(
                rx.el.span(coach["name"], font_weight="800", text_align="left"),
                rx.el.span(
                    coach["role"],
                    color=MUTED,
                    font_size="0.85rem",
                    text_align="left",
                ),
                rx.el.span(
                    coach["signature"],
                    color=coach["accent"],
                    font_size="0.8rem",
                    font_weight="800",
                    text_align="left",
                ),
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        type="button",
        on_click=select_coach(coach["id"]),
        width="100%",
        cursor="pointer",
        text_align="left",
        color=INK,
        font_family=BODY,
        padding="0.85rem",
        border_radius="18px",
        background_color=rx.cond(active, "rgba(214, 255, 60, 0.12)", "rgba(7, 10, 22, 0.72)"),
        border=rx.cond(active, "1px solid #d6ff3c", f"1px solid {LINE}"),
        backdrop_filter="blur(14px)",
    )


def principles() -> rx.Component:
    items = [
        ("Scale the load, not the standard", "The hour stays the hour. The weight changes. New athletes are not sent to a corner."),
        ("Names before numbers", "Coaches learn who you are before they learn your max. Leo starts that on Saturday."),
        ("Write it down", "The cycle exists before the room opens. You are not improvising your training in the doorway."),
    ]
    return rx.grid(
        *[
            glass(
                rx.el.h3(
                    title,
                    font_family=DISPLAY,
                    font_weight="700",
                    font_size="1.2rem",
                    letter_spacing="-0.03em",
                ),
                rx.el.p(copy, margin_top="0.45rem", color=MUTED, line_height="1.55"),
            )
            for title, copy in items
        ],
        columns=rx.breakpoints(initial="1", md="3"),
        spacing="3",
        width="100%",
    )


def coaches_page() -> rx.Component:
    return shell(
        rx.vstack(
            section_heading(
                "COACHES",
                "Six people. All of them on the floor.",
                "Pick a coach to read how they run their hour. Every one of them is on this week's board.",
            ),
            detail(),
            rx.grid(
                *[coach_card(coach) for coach in COACHES],
                columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                spacing="3",
                width="100%",
            ),
            principles(),
            spacing="5",
            width="100%",
            align="stretch",
        )
    )
