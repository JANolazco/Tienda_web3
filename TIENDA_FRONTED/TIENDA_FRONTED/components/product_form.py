import reflex as rx
from ..state import State

def modal_producto():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(rx.cond(State.form_id, "Editar producto", "Nuevo producto")),
            rx.vstack(
                rx.input(placeholder="Nombre", value=State.form_nombre, on_change=State.set_form_nombre),
                rx.input(placeholder="Descripción", value=State.form_descripcion, on_change=State.set_form_descripcion),
                rx.input(placeholder="Precio", value=State.form_precio, on_change=State.set_form_precio, type="number"),
                rx.button("Guardar", on_click=State.enviar_formulario, loading=State.cargando),
                spacing="3",
            ),
        ),
        open=State.modal_abierto,
    )