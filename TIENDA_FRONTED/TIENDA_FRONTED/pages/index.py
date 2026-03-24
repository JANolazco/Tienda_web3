import reflex as rx
from ..state import State
from ..components.product_form import modal_producto
from ..components.product_table import tabla_productos

def index():
    return rx.container(
        modal_producto(),
        rx.vstack(
            rx.heading("Gestión de Inventario", size="8"),
            rx.button("Nuevo Producto", on_click=State.abrir_modal_nuevo),
            rx.cond(State.cargando, rx.spinner(), tabla_productos()),
            align="center", spacing="5", padding_y="2em"
        ),
        on_mount=State.cargar_productos(1)
    )