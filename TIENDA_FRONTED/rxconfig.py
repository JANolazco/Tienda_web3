import reflex as rx

config = rx.Config(
    app_name="TIENDA_FRONTED",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)