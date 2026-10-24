"""Volt Atelier application entrypoint."""

import reflex as rx

from volt_atelier.mode import STATIC
from volt_atelier.pages.home import home_page

if STATIC:
    from volt_atelier.pages.static_coaches import coaches_page
    from volt_atelier.pages.static_lab import lab_page
    from volt_atelier.pages.static_membership import membership_page
    from volt_atelier.pages.static_schedule import schedule_page
else:
    from volt_atelier.pages.coaches import coaches_page
    from volt_atelier.pages.lab import lab_page
    from volt_atelier.pages.membership import membership_page
    from volt_atelier.pages.schedule import schedule_page
    from volt_atelier.state import StudioState


def _font_css() -> str:
    outfit = rx.asset("fonts/outfit.woff2")
    unbounded = rx.asset("fonts/unbounded.woff2")
    return f"""
@font-face {{
  font-family: "Outfit";
  font-style: normal;
  font-weight: 400 800;
  font-display: swap;
  src: url("{outfit}") format("woff2");
}}
@font-face {{
  font-family: "Unbounded";
  font-style: normal;
  font-weight: 500 900;
  font-display: swap;
  src: url("{unbounded}") format("woff2");
}}
"""


_icon = rx.asset("favicon.svg")
_share_image = rx.asset("background.jpg")

app = rx.App(
    stylesheets=["/styles.css"],
    html_lang="en",
    enable_state=not STATIC,
    head_components=[
        rx.el.link(rel="icon", href=_icon, type="image/svg+xml"),
        rx.el.style(_font_css()),
    ],
)

app.add_page(
    home_page,
    route="/",
    title="Volt Atelier — Boutique training in Port Meridian",
    description="A fictional boutique fitness studio with a weekly board, memberships, coaches, and a body lab.",
    image=_share_image,
)
_schedule_kwargs = {}
if not STATIC:
    _schedule_kwargs["on_load"] = StudioState.sync_lane
app.add_page(
    schedule_page,
    route="/schedule",
    title="The Week — Volt Atelier",
    description="Filter the Volt Atelier weekly class board by lane.",
    image=_share_image,
    **_schedule_kwargs,
)
app.add_page(
    membership_page,
    route="/membership",
    title="Membership — Volt Atelier",
    description="Spark, Current, and Kiln memberships, billed monthly or yearly.",
    image=_share_image,
)
app.add_page(
    coaches_page,
    route="/coaches",
    title="Coaches — Volt Atelier",
    description="The six coaches on the Volt Atelier floor.",
    image=_share_image,
)
app.add_page(
    lab_page,
    route="/lab",
    title="Body Lab — Volt Atelier",
    description="A BMI scale and a calorie target for training, not a diagnosis.",
    image=_share_image,
)
