import reflex as rx
from .pages.index import index

app = rx.App(
    theme=rx.theme(appearance="light", accent_color="blue")
)
app.add_page(index, title="Inventario - Tienda")