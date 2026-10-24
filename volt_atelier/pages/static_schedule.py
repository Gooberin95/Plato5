"""Weekly class board for the static Pages build."""

import reflex as rx

from volt_atelier.data import CLASSES, LANE_COLOR, LIME
from volt_atelier.frontend import (
    board_label,
    clear_class,
    day_is_empty,
    lane_filter,
    lane_is,
    lane_sync,
    selected_class,
    set_lane,
    toggle_class,
)
from volt_atelier.ui import (
    BODY,
    DISPLAY,
    FAINT,
    INK,
    INK_DARK,
    LINE,
    MUTED,
    glass,
    section_heading,
    shell,
)

DAYS = [
    ("Mon", "Monday"),
    ("Tue", "Tuesday"),
    ("Wed", "Wednesday"),
    ("Thu", "Thursday"),
    ("Fri", "Friday"),
    ("Sat", "Saturday"),
    ("Sun", "Sunday"),
]


def filter_bar() -> rx.Component:
    pills = [("All", LIME), *LANE_COLOR.items()]
    return rx.flex(
        *[
            rx.el.button(
                name,
                type="button",
                on_click=set_lane(name),
                cursor="pointer",
                border_radius="999px",
                padding="0.5rem 0.9rem",
                font_weight="800",
                font_size="0.88rem",
                font_family=BODY,
                white_space="nowrap",
                background_color=rx.cond(lane_filter.value == name, color, "rgba(7, 10, 22, 0.55)"),
                color=rx.cond(lane_filter.value == name, INK_DARK, INK),
                border=rx.cond(lane_filter.value == name, "1px solid transparent", f"1px solid {LINE}"),
                backdrop_filter="blur(10px)",
            )
            for name, color in pills
        ],
        wrap="wrap",
        spacing="2",
        width="100%",
    )


def class_card(item: dict) -> rx.Component:
    selected = selected_class.value == item["key"]
    return rx.cond(
        lane_is(item["type"]),
        rx.el.button(
            rx.box(width="100%", height="4px", border_radius="999px", background_color=item["accent"]),
            rx.flex(
                rx.el.span(item["time"], font_weight="800", font_size="0.82rem"),
                rx.el.span(item["minutes"], color=FAINT, font_size="0.75rem"),
                justify="between",
                align="center",
                width="100%",
            ),
            rx.el.span(item["name"], font_weight="800", font_size="0.98rem", line_height="1.25", text_align="left"),
            rx.el.span(
                item["type"],
                display="inline-flex",
                align_self="flex-start",
                border_radius="999px",
                padding="0.12rem 0.45rem",
                background_color=item["accent"],
                color=INK_DARK,
                font_size="0.68rem",
                font_weight="800",
                letter_spacing="0.04em",
            ),
            rx.el.span(item["coach"], color=MUTED, font_size="0.78rem", text_align="left"),
            type="button",
            on_click=toggle_class(item["key"]),
            width="100%",
            display="flex",
            flex_direction="column",
            align_items="stretch",
            gap="0.35rem",
            text_align="left",
            cursor="pointer",
            color=INK,
            font_family=BODY,
            padding="0.7rem",
            border_radius="16px",
            background_color=rx.cond(selected, "rgba(214, 255, 60, 0.14)", "rgba(255,255,255,0.04)"),
            border=rx.cond(selected, f"1px solid {LIME}", f"1px solid {LINE}"),
        ),
        rx.fragment(),
    )


def day_column(short: str, full: str) -> rx.Component:
    sessions = [item for item in CLASSES if item["day"] == short]
    return glass(
        rx.flex(
            rx.el.span(short, color=LIME, font_weight="800", letter_spacing="0.14em", font_size="0.75rem"),
            rx.el.span(full, color=FAINT, font_size="0.78rem"),
            justify="between",
            align="center",
            width="100%",
        ),
        rx.cond(
            day_is_empty(short),
            rx.el.p("Nothing in this lane.", margin_top="0.7rem", color=FAINT, font_size="0.85rem"),
            rx.fragment(),
        ),
        rx.vstack(*[class_card(item) for item in sessions], spacing="2", width="100%", margin_top="0.7rem"),
        pad="0.75rem",
    )


def _session_detail(item: dict) -> rx.Component:
    return rx.cond(
        selected_class.value == item["key"],
        glass(
            rx.flex(
                rx.box(
                    rx.el.p(item["type"], color=item["accent"], font_size="0.75rem", font_weight="800", letter_spacing="0.14em"),
                    rx.el.h3(item["name"], margin_top="0.25rem", font_family=DISPLAY, font_weight="800", font_size="1.7rem", letter_spacing="-0.03em"),
                    rx.el.p(item["day_full"], " · ", item["time"], " · ", item["minutes"], " · ", item["coach"], margin_top="0.35rem", color=MUTED),
                    rx.el.p(item["room"], " · ", item["spots"], " · ", item["level"], margin_top="0.2rem", color=FAINT, font_size="0.9rem"),
                    rx.el.p(item["blurb"], margin_top="0.7rem", line_height="1.55"),
                    flex="1",
                ),
                rx.el.button(
                    "Close",
                    type="button",
                    on_click=clear_class(),
                    cursor="pointer",
                    border_radius="999px",
                    padding="0.4rem 0.75rem",
                    font_weight="800",
                    font_family=BODY,
                    color=INK,
                    background_color="transparent",
                    border=f"1px solid {LINE}",
                    align_self="flex-start",
                ),
                direction=rx.breakpoints(initial="column", sm="row"),
                spacing="3",
                width="100%",
                align="start",
            ),
        ),
        rx.fragment(),
    )


def schedule_page() -> rx.Component:
    return shell(
        lane_sync(),
        rx.vstack(
            section_heading(
                "THE WEEK",
                "Twenty-six sessions. No filler hours.",
                "The board is the week. Filter it by lane, then open a session for the room, the cap, and the point of the hour.",
            ),
            filter_bar(),
            rx.el.p(board_label(), color=MUTED, font_weight="700"),
            rx.box(
                rx.cond(
                    selected_class.value == "",
                    glass(
                        rx.el.p("Pick a session.", font_family=DISPLAY, font_weight="700", font_size="1.25rem"),
                        rx.el.p(
                            "The plan, the room, and who it's for show up here. Filter the board by lane if you already know what you came for.",
                            margin_top="0.4rem",
                            color=MUTED,
                            line_height="1.55",
                        ),
                        pad="1rem",
                    ),
                    rx.fragment(),
                ),
                *[_session_detail(item) for item in CLASSES],
                width="100%",
            ),
            rx.grid(
                *[day_column(short, full) for short, full in DAYS],
                columns=rx.breakpoints(initial="1", sm="2", lg="3", xl="7"),
                spacing="3",
                width="100%",
            ),
            spacing="4",
            width="100%",
            align="stretch",
        ),
    )
