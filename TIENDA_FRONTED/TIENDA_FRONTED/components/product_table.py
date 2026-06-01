import reflex as rx
from ..state import State

def row_producto(producto: dict):
    return rx.table.row(
        rx.table.cell(producto["nombre"]),
        rx.table.cell(f"${producto['precio']}"),
        rx.table.cell(
            rx.hstack(
                rx.button(rx.icon("pencil"), on_click=lambda: State.abrir_modal_editar(producto), size="1"),
                rx.button(rx.icon("trash"), on_click=lambda: [State.set_producto_a_eliminar(producto), State.set_dialogo_eliminar_abierto(True)], color_scheme="red", size="1"),
            )
        )
    )

def tabla_productos():
    return rx.vstack(
        rx.table.root(
            rx.table.header(rx.table.row(rx.table.column_header_cell("Nombre"), rx.table.column_header_cell("Precio"), rx.table.column_header_cell("Acciones"))),
            rx.table.body(rx.foreach(State.productos, row_producto)),
            width="100%"
        ),
        rx.hstack(
            rx.button("Anterior", on_click=lambda: State.cargar_productos(State.pagina_actual - 1), disabled=State.pagina_actual <= 1),
            rx.text(f"Página {State.pagina_actual}"),
            rx.button("Siguiente", on_click=lambda: State.cargar_productos(State.pagina_actual + 1), disabled=State.siguiente_url == None),
            justify="center", width="100%"
        )
    )