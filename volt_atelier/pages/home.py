"""Home page: hero, lanes, house rules, testimonials, and a plan teaser."""

import reflex as rx

from volt_atelier.data import (
    COACH_COUNT,
    FEATURED,
    LANE_COUNT,
    LANE_INFO,
    PLANS,
    SESSION_COUNT,
    TESTIMONIALS,
)
from volt_atelier.ui import (
    DISPLAY,
    FAINT,
    INK,
    LIME,
    LINE,
    MUTED,
    billing_toggle,
    cta,
    glass,
    price_figure,
    section_heading,
    shell,
    stroke_row,
)


def hero() -> rx.Component:
    return rx.grid(
        glass(
            stroke_row(),
            rx.el.p(
                "PORT MERIDIAN · KILN LANE",
                margin_top="0.9rem",
                color=LIME,
                font_size="0.75rem",
                font_weight="800",
                letter_spacing="0.16em",
            ),
            rx.el.h1(
                rx.el.span("Small room.", display="block"),
                rx.el.span("Serious work.", display="block", color=LIME),
                margin_top="0.45rem",
                font_family=DISPLAY,
                font_weight="800",
                letter_spacing="-0.045em",
                line_height="0.9",
                font_size=rx.breakpoints(initial="3.1rem", md="4.8rem", lg="5.5rem"),
            ),
            rx.el.p(
                "Volt Atelier is a boutique training floor. Strength, conditioning, ride, mobility, and restore, in rooms of ten to sixteen. A coach can see your last rep. The week is written before you walk in.",
                margin_top="1rem",
                color=MUTED,
                font_size="1.08rem",
                line_height="1.6",
                max_width="38rem",
            ),
            rx.flex(
                cta("Book a trial class", "/membership#trial"),
                cta("See the week", "/schedule", ghost=True),
                spacing="3",
                wrap="wrap",
                margin_top="1.25rem",
            ),
            rx.el.p(
                "First class is free. A day pass is $32 if you want to look around first.",
                margin_top="0.9rem",
                color=FAINT,
                font_size="0.92rem",
            ),
            strong=True,
        ),
        rx.vstack(
            glass(
                rx.el.p(
                    "ON THE BOARD",
                    color=LIME,
                    font_size="0.72rem",
                    font_weight="800",
                    letter_spacing="0.16em",
                ),
                rx.el.p(
                    f"{FEATURED['time']} · {FEATURED['name']}",
                    margin_top="0.45rem",
                    font_family=DISPLAY,
                    font_weight="800",
                    font_size="1.55rem",
                    letter_spacing="-0.03em",
                    line_height="1.05",
                ),
                rx.el.p(
                    f"{FEATURED['coach']} · {FEATURED['room']} · {FEATURED['spots']}",
                    margin_top="0.4rem",
                    color=MUTED,
                ),
                rx.el.p(
                    FEATURED["blurb"],
                    margin_top="0.7rem",
                    line_height="1.55",
                ),
                rx.box(
                    cta("Ride this lane", "/schedule?lane=Ride", ghost=True),
                    margin_top="1rem",
                ),
            ),
            rx.grid(
                _stat(str(SESSION_COUNT), "sessions this week"),
                _stat("16", "athletes, max"),
                _stat(str(COACH_COUNT), "coaches on the floor"),
                _stat(str(LANE_COUNT), "lanes, one membership"),
                columns="2",
                spacing="3",
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        columns=rx.breakpoints(initial="1", lg="2"),
        spacing="4",
        width="100%",
        align="stretch",
    )


def _stat(value: str, label: str) -> rx.Component:
    return glass(
        rx.el.p(
            value,
            font_family=DISPLAY,
            font_weight="800",
            font_size="1.8rem",
            letter_spacing="-0.04em",
            line_height="1",
        ),
        rx.el.p(label, margin_top="0.35rem", color=MUTED, font_size="0.88rem"),
        pad="0.95rem",
    )


def lanes() -> rx.Component:
    return rx.box(
        section_heading(
            "THE FLOOR",
            "Five lanes. One building.",
            "Mix them or camp in one. The cap is the point: someone is watching the rep, not the front desk.",
        ),
        rx.grid(
            *[_lane_card(lane) for lane in LANE_INFO],
            columns=rx.breakpoints(initial="1", sm="2", lg="3"),
            spacing="3",
            width="100%",
            margin_top="1rem",
        ),
    )


def _lane_card(lane: dict) -> rx.Component:
    return rx.link(
        glass(
            rx.box(
                width="42px",
                height="8px",
                border_radius="999px",
                background_color=lane["accent"],
            ),
            rx.el.h3(
                lane["name"],
                margin_top="0.8rem",
                font_family=DISPLAY,
                font_weight="700",
                font_size="1.35rem",
                letter_spacing="-0.03em",
            ),
            rx.el.p(
                lane["line"],
                margin_top="0.45rem",
                color=MUTED,
                line_height="1.5",
            ),
            rx.el.p(
                lane["where"],
                margin_top="0.8rem",
                color=lane["accent"],
                font_weight="800",
                font_size="0.82rem",
                letter_spacing="0.04em",
            ),
            pad="1.05rem",
            _hover={"transform": "translateY(-2px)", "border_color": lane["accent"]},
            transition="transform 160ms ease, border-color 160ms ease",
        ),
        href=f"/schedule?lane={lane['name']}",
        text_decoration="none",
        color=INK,
        display="block",
    )


def rules() -> rx.Component:
    items = [
        ("01", "Sixteen is the ceiling", "When a class is full, it is full. The waitlist is real because the number is real."),
        ("02", "Coaches stay on the floor", "No headset in an office. The person who wrote the piece is close enough to fix your foot."),
        ("03", "The week changes", "Programming is posted before Monday. You should not be able to sleepwalk the workout."),
    ]
    return rx.grid(
        *[
            glass(
                rx.el.p(
                    number,
                    color=LIME,
                    font_family=DISPLAY,
                    font_weight="800",
                    letter_spacing="0.08em",
                ),
                rx.el.h3(
                    title,
                    margin_top="0.55rem",
                    font_family=DISPLAY,
                    font_weight="700",
                    font_size="1.35rem",
                    letter_spacing="-0.03em",
                ),
                rx.el.p(copy, margin_top="0.5rem", color=MUTED, line_height="1.55"),
            )
            for number, title, copy in items
        ],
        columns=rx.breakpoints(initial="1", md="3"),
        spacing="3",
        width="100%",
    )


def testimonials() -> rx.Component:
    return rx.box(
        section_heading("THE FLOOR, NOT A BILLBOARD", "What members actually say."),
        rx.grid(
            *[
                glass(
                    rx.el.p(
                        f"“{item['quote']}”",
                        line_height="1.55",
                        font_size="1.02rem",
                    ),
                    rx.el.p(
                        item["name"],
                        margin_top="0.9rem",
                        font_weight="800",
                    ),
                    rx.el.p(item["meta"], color=FAINT, font_size="0.85rem"),
                    pad="1.05rem",
                )
                for item in TESTIMONIALS
            ],
            columns=rx.breakpoints(initial="1", sm="2", lg="3"),
            spacing="3",
            width="100%",
            margin_top="1rem",
        ),
    )


def plan_teaser() -> rx.Component:
    return glass(
        rx.flex(
            rx.box(
                section_heading(
                    "MEMBERSHIP",
                    "Pick a pace.",
                    "Spark if you visit. Current if you live here. Kiln if you want the plan written with your name on it.",
                ),
            ),
            billing_toggle(),
            direction=rx.breakpoints(initial="column", lg="row"),
            justify="between",
            align=rx.breakpoints(initial="start", lg="end"),
            spacing="4",
            width="100%",
        ),
        rx.grid(
            *[
                rx.box(
                    rx.el.p(
                        plan["name"],
                        font_family=DISPLAY,
                        font_weight="800",
                        font_size="1.2rem",
                    ),
                    rx.el.p(plan["kicker"], color=FAINT, font_size="0.85rem", margin_top="0.2rem"),
                    rx.box(
                        price_figure(plan["monthly"], plan["yearly_month"], "2.2rem"),
                        margin_top="0.7rem",
                    ),
                    padding="0.9rem",
                    border_radius="16px",
                    border=f"1px solid {LIME}" if plan["featured"] else f"1px solid {LINE}",
                    background_color="rgba(255,255,255,0.03)",
                )
                for plan in PLANS
            ],
            columns=rx.breakpoints(initial="1", md="3"),
            spacing="3",
            width="100%",
            margin_top="1rem",
        ),
        rx.box(
            cta("Compare the three plans", "/membership"),
            margin_top="1rem",
        ),
        strong=True,
    )


def home_page() -> rx.Component:
    return shell(
        rx.vstack(
            hero(),
            lanes(),
            rx.box(
                section_heading("HOUSE RULES", "How the room actually runs."),
                rules(),
                width="100%",
            ),
            testimonials(),
            plan_teaser(),
            spacing="6",
            width="100%",
            align="stretch",
        )
    )
