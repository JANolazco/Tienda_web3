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

def dialogo_eliminar():
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Eliminar Producto"),
            rx.alert_dialog.description(
                rx.cond(
                    State.producto_a_eliminar,
                    rx.text(f"¿Estás seguro que deseas eliminar '{State.producto_a_eliminar['nombre']}'?"),
                    rx.text("Cargando...")
                )
            ),
            rx.hstack(
                rx.alert_dialog.cancel(rx.button("Cancelar")),
                rx.alert_dialog.action(rx.button("Eliminar", color_scheme="red", on_click=State.eliminar_producto_confirmado)),
            ),
        ),
        open=State.dialogo_eliminar_abierto,
    )