# REPORTE_ERRORES.md

## Objetivo

Este documento resume los errores y riesgos que encontre al revisar el codigo del proyecto, junto con una propuesta de subsanacion para cada caso.

No modifica el codigo. Solo sirve como guia tecnica para corregir el sistema de forma ordenada.

---

## 1) Mismatch entre frontend y backend en PUT/DELETE

**Ubicacion**
- `TIENDA_FRONTED/TIENDA_FRONTED/state.py`
- `BACKEND/inventario/urls.py`

**Que pasa**
- El frontend construye URLs como `http://localhost:8000/api/v1/tienda/{id}/`.
- El backend expone la ruta como `v1/tienda/<int:id>` sin slash final.

**Por que es un problema**
- Las llamadas de editar y borrar pueden terminar en 404 dependiendo del cliente y del comportamiento de redireccion.
- El flujo principal de la UI queda inconsistente aunque el API exista.

**Propuesta de subsanacion**
1. Unificar el formato de rutas en todo el proyecto.
2. Elegir una sola convension:
   - o el backend acepta slash final,
   - o el frontend elimina el slash final.
3. Mantener la misma convension para GET, POST, PUT y DELETE.

**Implementacion sugerida**
- Ajustar la ruta del backend para aceptar slash final de forma consistente.
- O ajustar el frontend para construir `.../{id}` en lugar de `.../{id}/`.

---

## 2) La API de inventario sigue publica

**Ubicacion**
- `BACKEND/inventario_api/settings.py`
- `BACKEND/inventario/views.py`

**Que pasa**
- En settings ya se activa `JWTAuthentication`.
- Pero las vistas de inventario no tienen `permission_classes = [IsAuthenticated]`.

**Por que es un problema**
- Cualquier cliente anonimo puede listar, crear, editar y borrar productos.
- Tener autenticacion configurada pero no aplicada da una falsa sensacion de seguridad.

**Propuesta de subsanacion**
1. Proteger las vistas del inventario con permisos autenticados.
2. Definir si toda la API sera privada o si algunas operaciones seran publicas.
3. En frontend, enviar el token en el header `Authorization: Bearer <token>`.

**Implementacion sugerida**
- Agregar `permission_classes = [IsAuthenticated]` a las vistas del inventario.
- Si se requiere acceso publico solo para lectura, separar permisos por metodo HTTP.

---

## 3) Flujo de autenticacion incompleto y riesgoso

**Ubicacion**
- `BACKEND/inventario_api/serializers.py`
- `BACKEND/inventario_api/views.py`

**Que pasa**
- El serializer de usuario expone el campo `password`.
- `register` guarda el usuario y responde con `serial.data`, lo que puede incluir el password.
- `login` no emite JWT, solo devuelve datos del usuario.
- `login` asume que `username` y `password` siempre existen en `request.data`.

**Por que es un problema**
- Exponer passwords en respuestas es un riesgo severo.
- El login no entrega un mecanismo real de sesion para proteger la API.
- Una peticion mal formada puede provocar errores por claves faltantes.

**Propuesta de subsanacion**
1. Nunca devolver `password` en respuestas.
2. Separar serializer de registro y serializer de lectura.
3. Emitir `access` y `refresh` tokens en login.
4. Validar entrada antes de acceder a `request.data["username"]` o `request.data["password"]`.

**Implementacion sugerida**
- Crear un serializer de auth con `password` solo para escritura.
- Marcar `password` como `write_only`.
- En login, usar `TokenObtainPairSerializer` o generar JWT manualmente con SimpleJWT.

---

## 4) App `Ticket` con errores de formularios y flujo

**Ubicacion**
- `BACKEND/Ticket/forms.py`
- `BACKEND/Ticket/views.py`

**Que pasa**
- En los `ModelForm` se usa `field` en lugar de `fields`.
- `TicketForm` no define correctamente sus campos.
- `TicketItemForm` tiene `field=['producto,cantidad']`, que es una lista con una sola cadena invalida.
- En la vista `crear_ticket`, `messages.error(...)` usa una firma incorrecta.
- La logica de rollback y `return` esta dentro del ciclo, por lo que la transaccion se corta antes de procesar items de forma correcta.

**Por que es un problema**
- El formulario puede fallar al construirse.
- La vista no procesa el ticket de manera confiable.
- El comportamiento actual no garantiza consistencia de stock ni de items.

**Propuesta de subsanacion**
1. Corregir `fields` en ambos formularios.
2. Definir bien la forma del formset.
3. Reestructurar `crear_ticket` para:
   - validar todos los items,
   - verificar stock,
   - crear ticket e items solo si todo es valido,
   - hacer rollback si algo falla.

**Implementacion sugerida**
- Usar `fields = []` o los campos correctos en `TicketForm`.
- Usar `fields = ["producto", "cantidad"]` en `TicketItemForm`.
- Mover el `return` y el control de rollback fuera del loop.
- Llamar `messages.error(request, mensaje)` con la firma correcta.

---

## 5) Paginacion desconectada entre backend y frontend

**Ubicacion**
- `BACKEND/inventario/views.py`
- `TIENDA_FRONTED/TIENDA_FRONTED/state.py`
- `TIENDA_FRONTED/TIENDA_FRONTED/components/product_table.py`

**Que pasa**
- El backend devuelve una lista simple de productos.
- El frontend espera una respuesta paginada con `count`, `results`, `next` y `previous`.
- El estado calcula paginas usando esos campos, pero normalmente no los recibe.

**Por que es un problema**
- Los botones de navegacion pueden quedar inutiles.
- La logica de pagina actual y siguiente url no se sostiene.
- El frontend asume un contrato de API que el backend no cumple.

**Propuesta de subsanacion**
1. Decidir si la API sera paginada o no.
2. Si se quiere paginacion real, implementarla en backend.
3. Si se quiere lista simple, simplificar el frontend para no esperar metadatos de paginacion.

**Implementacion sugerida**
- En backend, usar paginacion de DRF y devolver `count`, `results`, `next`, `previous`.
- En frontend, leer esa estructura y deshabilitar el boton siguiente cuando `next` sea `None`.

---

## 6) `Meta` duplicada en `ListaProducto`

**Ubicacion**
- `BACKEND/inventario/models.py`

**Que pasa**
- El modelo tiene dos clases `Meta`.
- En Python, la segunda sobrescribe la primera.

**Por que es un problema**
- `verbose_name` y `verbose_name_plural` no se aplican.
- La intencion del modelo queda incompleta y confusa.

**Propuesta de subsanacion**
1. Unificar toda la configuracion de `Meta` en una sola clase.
2. Mantener juntos `verbose_name`, `verbose_name_plural` y `ordering`.

**Implementacion sugerida**
- Dejar una sola `class Meta:` con todos los atributos necesarios.

---

## 7) Configuracion de CORS inconsistente

**Ubicacion**
- `BACKEND/inventario_api/settings.py`

**Que pasa**
- Se define `CORS_ALLOW_ALL_ORIGINS = True`.
- Justo despues aparece una lista suelta con `["http://localhost:3000"]` que no esta asignada a ninguna variable.

**Por que es un problema**
- Esa lista no tiene efecto.
- Puede confundir a cualquiera que revise la configuracion.
- No deja claro si el proyecto usa CORS abierto o una whitelist especifica.

**Propuesta de subsanacion**
1. Elegir una sola politica de CORS.
2. Si es desarrollo, usar `CORS_ALLOW_ALL_ORIGINS = True`.
3. Si se quiere restringir, usar `CORS_ALLOWED_ORIGINS = [...]`.

**Implementacion sugerida**
- Eliminar la lista suelta.
- Reemplazarla por la configuracion correcta segun el entorno.

---

## Prioridad recomendada

1. Corregir el mismatch de rutas frontend/backend.
2. Proteger la API con permisos y arreglar el flujo de auth.
3. Reparar `Ticket` si esa funcionalidad sigue en alcance.
4. Sincronizar la paginacion entre backend y frontend.
5. Limpiar el modelo `Meta` duplicado y la config de CORS.

---

## Resumen ejecutivo

El proyecto esta bastante avanzado en la parte de CRUD principal, pero tiene tres riesgos fuertes:

- Seguridad incompleta.
- Inconsistencias de contrato entre frontend y backend.
- Una funcionalidad adicional (`Ticket`) con errores de implementacion.

La mejor estrategia es corregir primero la base funcional y de seguridad, luego limpiar la parte secundaria.
