import reflex as rx

config = rx.Config(
    app_name="volt_atelier",
    show_built_with_reflex=False,
    default_color_mode="dark",
    disable_plugins=[rx.plugins.SitemapPlugin],
    plugins=[
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="dark",
                accent_color="lime",
                gray_color="slate",
                radius="large",
                has_background=True,
            )
        )
    ],
)
