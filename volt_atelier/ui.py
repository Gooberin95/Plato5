"""Shared chrome, type, and card styles for Volt Atelier."""

import reflex as rx

from volt_atelier.data import (
    COACH_COUNT,
    HOURS,
    INK,
    INK_DARK,
    LANE_COUNT,
    LANE_INFO,
    LIME,
    NAV,
    ORANGE,
    SESSION_COUNT,
    VISIT,
    BLUE,
    GREEN,
    YELLOW,
)
from volt_atelier.state import StudioState

DISPLAY = "Unbounded, sans-serif"
BODY = "Outfit, sans-serif"
MUTED = "rgba(246, 243, 236, 0.78)"
FAINT = "rgba(246, 243, 236, 0.64)"
LINE = "rgba(255, 255, 255, 0.12)"
GLASS = "rgba(7, 10, 22, 0.78)"
GLASS_STRONG = "rgba(5, 8, 18, 0.88)"


def glass(*children, strong: bool = False, pad: str = "1.2rem", **props) -> rx.Component:
    base = {
        "background_color": GLASS_STRONG if strong else GLASS,
        "backdrop_filter": "blur(16px)",
        "border": f"1px solid {LINE}",
        "border_radius": "22px",
        "padding": pad,
        "width": "100%",
        "box_shadow": "0 18px 50px rgba(0, 0, 0, 0.28)",
    }
    base.update(props)
    return rx.box(*children, **base)


def stroke_row() -> rx.Component:
    marks = [
        (ORANGE, "-12"),
        (BLUE, "8"),
        (LIME, "-6"),
        (YELLOW, "14"),
        (GREEN, "-8"),
    ]
    return rx.flex(
        *[
            rx.box(
                width="26px",
                height="8px",
                border_radius="999px",
                background_color=color,
                transform=f"rotate({angle}deg)",
                flex_shrink="0",
            )
            for color, angle in marks
        ],
        spacing="2",
        align="center",
    )


def mark() -> rx.Component:
    bars = [(ORANGE, "-16"), (BLUE, "10"), (LIME, "-6"), (YELLOW, "16")]
    return rx.flex(
        *[
            rx.box(
                width="6px",
                height="16px",
                border_radius="999px",
                background_color=color,
                transform=f"rotate({angle}deg)",
            )
            for color, angle in bars
        ],
        spacing="1",
        align="center",
        justify="center",
        width="42px",
        height="36px",
        border_radius="12px",
        background_color="rgba(7, 10, 22, 0.72)",
        border=f"1px solid {LINE}",
        flex_shrink="0",
    )


def cta(label: str, href: str, ghost: bool = False) -> rx.Component:
    if ghost:
        background = "rgba(7, 10, 22, 0.45)"
        color = INK
        border = f"1px solid {LINE}"
    else:
        background = LIME
        color = INK_DARK
        border = "1px solid transparent"
    return rx.link(
        label,
        href=href,
        display="inline-flex",
        align_items="center",
        justify_content="center",
        background_color=background,
        color=color,
        border=border,
        border_radius="999px",
        padding="0.8rem 1.15rem",
        font_weight="800",
        text_decoration="none",
        white_space="nowrap",
        backdrop_filter="blur(10px)",
        transition="transform 160ms ease",
        _hover={"transform": "translateY(-1px)"},
    )


def nav_link(label: str, href: str) -> rx.Component:
    active = StudioState.nav_path == href
    return rx.link(
        label,
        href=href,
        aria_current=rx.cond(active, "page", "false"),
        display="inline-flex",
        align_items="center",
        justify_content="center",
        border_radius="999px",
        padding_x=rx.breakpoints(initial="0.68rem", sm="0.9rem"),
        padding_y="0.52rem",
        font_weight="800",
        font_size=rx.breakpoints(initial="0.8rem", sm="0.92rem"),
        text_decoration="none",
        white_space="nowrap",
        background_color=rx.cond(active, LIME, "transparent"),
        color=rx.cond(active, INK_DARK, INK),
    )


def topbar() -> rx.Component:
    return rx.el.header(
        rx.flex(
            rx.link(
                rx.flex(
                    mark(),
                    rx.box(
                        rx.el.span(
                            "VOLT ATELIER",
                            font_family=DISPLAY,
                            font_weight="800",
                            font_size="0.78rem",
                            letter_spacing="0.12em",
                            color=INK,
                        ),
                        rx.el.span(
                            "PORT MERIDIAN",
                            display=rx.breakpoints(initial="none", sm="block"),
                            color=FAINT,
                            font_size="0.68rem",
                            letter_spacing="0.14em",
                            font_weight="700",
                        ),
                    ),
                    spacing="3",
                    align="center",
                ),
                href="/",
                text_decoration="none",
            ),
            rx.box(flex="1"),
            rx.el.span(
                VISIT["address"],
                display=rx.breakpoints(initial="none", md="inline"),
                color=MUTED,
                font_size="0.92rem",
            ),
            cta("Book a trial", "/membership#trial"),
            width="100%",
            align="center",
            spacing="3",
        ),
        position="fixed",
        top="0",
        left="0",
        right="0",
        z_index="40",
        padding_x=rx.breakpoints(initial="0.9rem", md="1.4rem"),
        padding_y="0.75rem",
        background_color="rgba(6, 10, 22, 0.72)",
        backdrop_filter="blur(18px)",
        border_bottom=f"1px solid {LINE}",
    )


def pill_nav() -> rx.Component:
    return rx.box(
        rx.el.nav(
            rx.flex(
                *[nav_link(label, href) for label, href in NAV],
                spacing="1",
                align="center",
            ),
            aria_label="Primary",
            background_color="rgba(6, 10, 22, 0.8)",
            backdrop_filter="blur(18px)",
            border=f"1px solid {LINE}",
            border_radius="999px",
            padding="0.35rem",
            box_shadow="0 16px 50px rgba(0, 0, 0, 0.45)",
            pointer_events="auto",
            max_width="calc(100vw - 1rem)",
            overflow_x="auto",
            class_name="pill-scroll",
        ),
        position="fixed",
        bottom="0.85rem",
        left="0",
        right="0",
        z_index="50",
        display="flex",
        justify_content="center",
        pointer_events="none",
    )


def footer() -> rx.Component:
    return rx.el.footer(
        glass(
            rx.grid(
                rx.box(
                    rx.flex(mark(), spacing="3", align="center"),
                    rx.el.p(
                        "VOLT ATELIER",
                        margin_top="0.8rem",
                        font_family=DISPLAY,
                        font_weight="800",
                        letter_spacing="0.08em",
                        font_size="0.95rem",
                    ),
                    rx.el.p(
                        "A 10-to-16 person floor for people who like their training loud, precise, and finished.",
                        margin_top="0.45rem",
                        color=MUTED,
                        line_height="1.55",
                    ),
                ),
                rx.box(
                    rx.el.p(
                        "VISIT",
                        color=LIME,
                        font_size="0.72rem",
                        font_weight="800",
                        letter_spacing="0.14em",
                    ),
                    rx.el.p(VISIT["address"], margin_top="0.55rem", font_weight="700"),
                    rx.el.p(VISIT["city"], color=MUTED),
                    rx.el.p(VISIT["phone"], margin_top="0.45rem", color=MUTED),
                    rx.el.p(VISIT["email"], color=MUTED),
                ),
                rx.box(
                    rx.el.p(
                        "HOURS",
                        color=LIME,
                        font_size="0.72rem",
                        font_weight="800",
                        letter_spacing="0.14em",
                    ),
                    *[
                        rx.flex(
                            rx.el.span(label, color=MUTED),
                            rx.el.span(value, font_weight="700"),
                            justify="between",
                            width="100%",
                            margin_top="0.4rem",
                            spacing="3",
                        )
                        for label, value in HOURS
                    ],
                ),
                rx.box(
                    rx.el.p(
                        "LANES",
                        color=LIME,
                        font_size="0.72rem",
                        font_weight="800",
                        letter_spacing="0.14em",
                    ),
                    *[
                        rx.link(
                            lane["name"],
                            href=f"/schedule?lane={lane['name']}",
                            display="block",
                            margin_top="0.4rem",
                            color=INK,
                            text_decoration="none",
                            font_weight="700",
                        )
                        for lane in LANE_INFO
                    ],
                ),
                columns=rx.breakpoints(initial="1", sm="2", lg="4"),
                spacing="5",
                width="100%",
            ),
            rx.el.p(
                f"{SESSION_COUNT} sessions · {COACH_COUNT} coaches · {LANE_COUNT} lanes. Volt Atelier is a fictional studio. The trial form stays in this browser session and is not sent anywhere.",
                margin_top="1.1rem",
                color=FAINT,
                font_size="0.82rem",
                line_height="1.5",
            ),
            strong=True,
        ),
        margin_top="1.5rem",
    )


def shell(*children) -> rx.Component:
    """Page root. The painting is applied once here and stays fixed while scrolling."""
    return rx.box(
        topbar(),
        rx.el.main(
            *children,
            footer(),
            width="100%",
            max_width="1240px",
            margin_x="auto",
            padding_x=rx.breakpoints(initial="1rem", md="1.4rem"),
            padding_top="5.7rem",
            padding_bottom="7.6rem",
        ),
        pill_nav(),
        background_image="url(/background.jpg)",
        background_size="cover",
        background_position="center",
        background_attachment="fixed",
        background_repeat="no-repeat",
        background_color="#070b16",
        min_height="100vh",
        width="100%",
        color=INK,
        font_family=BODY,
    )


def section_heading(kicker: str, title: str, copy: str = "") -> rx.Component:
    parts: list[rx.Component] = [
        stroke_row(),
        rx.el.p(
            kicker,
            margin_top="0.75rem",
            color=LIME,
            font_size="0.75rem",
            font_weight="800",
            letter_spacing="0.16em",
        ),
        rx.el.h2(
            title,
            margin_top="0.35rem",
            font_family=DISPLAY,
            font_weight="800",
            letter_spacing="-0.04em",
            line_height="0.98",
            font_size=rx.breakpoints(initial="2.05rem", md="2.9rem"),
        ),
    ]
    if copy:
        parts.append(
            rx.el.p(
                copy,
                margin_top="0.7rem",
                color=MUTED,
                max_width="42rem",
                line_height="1.6",
                font_size="1.05rem",
            )
        )
    return rx.box(*parts)


def field_label(text: str) -> rx.Component:
    return rx.el.p(
        text,
        color=FAINT,
        font_size="0.75rem",
        font_weight="800",
        letter_spacing="0.12em",
    )


def text_field(value, on_change, placeholder: str) -> rx.Component:
    return rx.input(
        value=value,
        on_change=on_change,
        placeholder=placeholder,
        type="text",
        width="100%",
        size="3",
        variant="soft",
        color_scheme="gray",
        radius="large",
    )


def choice_row(options: list[tuple[str, str]], current, setter) -> rx.Component:
    return rx.flex(
        *[
            rx.el.button(
                label,
                type="button",
                on_click=setter(value),
                cursor="pointer",
                border_radius="999px",
                padding="0.48rem 0.8rem",
                font_weight="800",
                font_size="0.86rem",
                font_family=BODY,
                white_space="nowrap",
                background_color=rx.cond(current == value, LIME, "rgba(255,255,255,0.04)"),
                color=rx.cond(current == value, INK_DARK, INK),
                border=rx.cond(
                    current == value,
                    "1px solid transparent",
                    f"1px solid {LINE}",
                ),
            )
            for value, label in options
        ],
        wrap="wrap",
        spacing="2",
        width="100%",
    )


def billing_toggle() -> rx.Component:
    return rx.flex(
        rx.el.button(
            "Monthly",
            type="button",
            on_click=StudioState.show_monthly,
            cursor="pointer",
            border_radius="999px",
            padding="0.5rem 0.95rem",
            font_weight="800",
            font_family=BODY,
            background_color=rx.cond(StudioState.yearly, "transparent", LIME),
            color=rx.cond(StudioState.yearly, INK, INK_DARK),
            border=rx.cond(StudioState.yearly, f"1px solid {LINE}", "1px solid transparent"),
        ),
        rx.el.button(
            "Yearly",
            type="button",
            on_click=StudioState.show_yearly,
            cursor="pointer",
            border_radius="999px",
            padding="0.5rem 0.95rem",
            font_weight="800",
            font_family=BODY,
            background_color=rx.cond(StudioState.yearly, LIME, "transparent"),
            color=rx.cond(StudioState.yearly, INK_DARK, INK),
            border=rx.cond(StudioState.yearly, "1px solid transparent", f"1px solid {LINE}"),
        ),
        rx.el.span(
            "Save up to $528 a year",
            color=LIME,
            font_size="0.85rem",
            font_weight="700",
            align_self="center",
        ),
        spacing="2",
        align="center",
        wrap="wrap",
    )


def price_figure(monthly: int, yearly_month: int, size: str = "3rem") -> rx.Component:
    return rx.flex(
        rx.el.span(
            rx.cond(StudioState.yearly, f"${yearly_month}", f"${monthly}"),
            font_family=DISPLAY,
            font_weight="800",
            font_size=size,
            letter_spacing="-0.045em",
            line_height="0.9",
        ),
        rx.el.span(
            rx.cond(StudioState.yearly, "/mo, billed yearly", "/month"),
            color=MUTED,
            font_size="0.92rem",
            padding_bottom="0.35rem",
        ),
        spacing="2",
        align="end",
    )
