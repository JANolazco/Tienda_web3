import reflex as rx
import httpx
import urllib.parse

API_URL = "http://localhost:8000/api/v1/tienda/"

class State(rx.State):
    productos: list[dict] = []
    pagina_actual: int = 1
    total_paginas: int = 1
    siguiente_url: str | None = None
    anterior_url: str | None = None

    form_id: int | None = None
    form_nombre: str = ""
    form_descripcion: str = ""
    form_precio: str = ""
    modal_abierto: bool = False

    producto_a_eliminar: dict | None = None
    dialogo_eliminar_abierto: bool = False

    cargando: bool = False
    toast_titulo: str = ""
    toast_descripcion: str = ""
    toast_tipo: str = "info"
    toast_visible: bool = False

    error_nombre: str = ""
    error_precio: str = ""

    def set_form_nombre(self, value: str): self.form_nombre = value
    def set_form_descripcion(self, value: str): self.form_descripcion = value
    def set_form_precio(self, value: str): self.form_precio = value

    async def cargar_productos(self, pagina: int = 1):
        self.cargando = True
        self.toast_visible = False
        url = f"{API_URL}?page={pagina}" if pagina > 1 else API_URL
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, dict) and "results" in data:
                        self.productos = data["results"]
                        self.total_paginas = (data["count"] + 9) // 10
                        self.siguiente_url = data.get("next")
                        self.anterior_url = data.get("previous")
                    else:
                        self.productos = data if isinstance(data, list) else []
                        self.total_paginas = 1
                    self.pagina_actual = pagina
            except Exception as ex:
                self.mostrar_toast("Error", str(ex), "error")
            finally:
                self.cargando = False

    async def enviar_formulario(self):
        if not self.form_nombre.strip() or not self.form_precio:
            self.error_nombre = "Requerido" if not self.form_nombre.strip() else ""
            return
        
        data = {
            "nombre": self.form_nombre.strip(),
            "descripcion": self.form_descripcion.strip(),
            "precio": float(self.form_precio)
        }
        
        url = f"{API_URL}{self.form_id}/" if self.form_id else API_URL
        method = "PUT" if self.form_id else "POST"

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.request(method, url, json=data)
                if resp.status_code in (200, 201):
                    self.modal_abierto = False
                    await self.cargar_productos(self.pagina_actual)
            except Exception as ex:
                self.mostrar_toast("Error", str(ex), "error")

    async def eliminar_producto_confirmado(self):
        if not self.producto_a_eliminar: return
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.delete(f"{API_URL}{self.producto_a_eliminar['id']}/")
                if resp.status_code == 204:
                    self.dialogo_eliminar_abierto = False
                    await self.cargar_productos(self.pagina_actual)
            except Exception: pass

    def abrir_modal_nuevo(self):
        self.form_id, self.form_nombre, self.form_descripcion, self.form_precio = None, "", "", ""
        self.modal_abierto = True

    def abrir_modal_editar(self, producto: dict):
        self.form_id, self.form_nombre = producto["id"], producto["nombre"]
        self.form_descripcion, self.form_precio = producto.get("descripcion", ""), str(producto["precio"])
        self.modal_abierto = True

    def mostrar_toast(self, titulo, desc, tipo):
        self.toast_titulo, self.toast_descripcion, self.toast_tipo, self.toast_visible = titulo, desc, tipo, True