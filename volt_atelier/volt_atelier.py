"""Volt Atelier application entrypoint."""

import reflex as rx

from volt_atelier.pages.coaches import coaches_page
from volt_atelier.pages.home import home_page
from volt_atelier.pages.lab import lab_page
from volt_atelier.pages.membership import membership_page
from volt_atelier.pages.schedule import schedule_page
from volt_atelier.state import StudioState

app = rx.App(
    stylesheets=["/styles.css"],
    html_lang="en",
    head_components=[
        rx.el.link(rel="icon", href="/favicon.svg", type="image/svg+xml"),
    ],
)

app.add_page(
    home_page,
    route="/",
    title="Volt Atelier — Boutique training in Port Meridian",
    description="A fictional boutique fitness studio with a weekly board, memberships, coaches, and a body lab.",
    image="/background.jpg",
)
app.add_page(
    schedule_page,
    route="/schedule",
    title="The Week — Volt Atelier",
    description="Filter the Volt Atelier weekly class board by lane.",
    on_load=StudioState.sync_lane,
    image="/background.jpg",
)
app.add_page(
    membership_page,
    route="/membership",
    title="Membership — Volt Atelier",
    description="Spark, Current, and Kiln memberships, billed monthly or yearly.",
    image="/background.jpg",
)
app.add_page(
    coaches_page,
    route="/coaches",
    title="Coaches — Volt Atelier",
    description="The six coaches on the Volt Atelier floor.",
    image="/background.jpg",
)
app.add_page(
    lab_page,
    route="/lab",
    title="Body Lab — Volt Atelier",
    description="A BMI scale and calorie target for training, not a diagnosis.",
    image="/background.jpg",
)
