# PLAN_PARA_SUBSANAR_LOS_ERRORES_ENCONTRADOS_EN_EL_ARCHIVO_REPORTE_ERRORES

## Objetivo

Corregir los errores detectados en el reporte previo, en orden de prioridad, sin introducir cambios innecesarios.

## Criterio general de trabajo

- Corregir primero los fallos que rompen el flujo principal.
- Luego cerrar los riesgos de seguridad.
- Despues reparar la funcionalidad secundaria y la consistencia tecnica.
- Validar cada cambio con pruebas o verificacion manual antes de pasar al siguiente.

## Orden de ejecucion

1. Unificar rutas entre frontend y backend.
2. Proteger la API de inventario con permisos reales.
3. Corregir el flujo de autenticacion.
4. Reparar el modulo `Ticket`.
5. Alinear la paginacion entre frontend y backend.
6. Unificar la clase `Meta` del modelo `ListaProducto`.
7. Limpiar la configuracion de CORS.

---

## Tarea 1: Unificar rutas entre frontend y backend

- Objetivo: evitar 404 en las acciones de editar y borrar desde la UI.
- Archivos involucrados: `TIENDA_FRONTED/TIENDA_FRONTED/state.py`, `BACKEND/inventario/urls.py`.
- Problema a resolver: el frontend envia `.../{id}/` y el backend expone `.../<int:id>` sin slash final.
- Pasos:
  1. Elegir una sola convension para las rutas.
  2. Aplicar la misma convension en frontend y backend.
  3. Revisar que GET, POST, PUT y DELETE sigan el mismo patron.
- Validacion:
  - Editar un producto desde la UI funciona.
  - Eliminar un producto desde la UI funciona.
  - No aparecen 404 por diferencias de slash final.
- Resultado esperado: contrato de rutas consistente en toda la app.

---

## Tarea 2: Proteger la API de inventario

- Objetivo: impedir acceso anonimo a lectura y escritura de productos, si ese es el modelo de seguridad deseado.
- Archivos involucrados: `BACKEND/inventario_api/settings.py`, `BACKEND/inventario/views.py`.
- Problema a resolver: JWT esta configurado, pero las vistas no exigen autenticacion.
- Pasos:
  1. Definir si la API sera privada total o parcialmente publica.
  2. Agregar permisos autenticados a las vistas de inventario.
  3. En caso de permisos por metodo, separar lectura y escritura segun corresponda.
- Validacion:
  - Una peticion sin token no puede modificar productos.
  - Una peticion autenticada si puede operar segun la politica definida.
- Resultado esperado: la API responde solo a usuarios autorizados.

---

## Tarea 3: Corregir el flujo de autenticacion

- Objetivo: evitar exposicion de credenciales y emitir tokens validos.
- Archivos involucrados: `BACKEND/inventario_api/serializers.py`, `BACKEND/inventario_api/views.py`.
- Problema a resolver: el serializer expone `password` y el login no devuelve JWT.
- Pasos:
  1. Separar serializer de escritura y serializer de lectura.
  2. Marcar `password` como `write_only`.
  3. Evitar devolver `serial.data` con campos sensibles.
  4. Hacer que el login entregue `access` y `refresh`.
  5. Validar que `username` y `password` existan antes de usarlos.
- Validacion:
  - El password nunca aparece en una respuesta JSON.
  - El login retorna tokens.
  - Una peticion incompleta no rompe la vista.
- Resultado esperado: autenticacion funcional y segura.

---

## Tarea 4: Reparar el modulo `Ticket`

- Objetivo: dejar funcional la creacion de tickets y el descuento de stock.
- Archivos involucrados: `BACKEND/Ticket/forms.py`, `BACKEND/Ticket/views.py`.
- Problema a resolver: los formularios usan `field` en vez de `fields`, y la vista tiene flujo roto.
- Pasos:
  1. Corregir `fields` en `TicketForm`.
  2. Corregir `fields` en `TicketItemForm`.
  3. Revisar la definicion del `inlineformset_factory`.
  4. Reestructurar `crear_ticket` para validar todo antes de crear registros.
  5. Mover el control de rollback y los `return` fuera del ciclo de items.
  6. Corregir la llamada a `messages.error`.
- Validacion:
  - El formulario se renderiza sin error.
  - El ticket se crea solo si todos los items son validos.
  - El stock se descuenta correctamente.
  - La transaccion se revierte si algo falla.
- Resultado esperado: flujo de tickets estable y consistente.

---

## Tarea 5: Alinear la paginacion entre frontend y backend

- Objetivo: hacer que la navegacion por paginas funcione de forma real.
- Archivos involucrados: `BACKEND/inventario/views.py`, `TIENDA_FRONTED/TIENDA_FRONTED/state.py`, `TIENDA_FRONTED/TIENDA_FRONTED/components/product_table.py`.
- Problema a resolver: el backend devuelve una lista simple y el frontend espera `count`, `results`, `next` y `previous`.
- Pasos:
  1. Decidir si la API tendra paginacion o no.
  2. Si la respuesta es paginada, implementarla en backend.
  3. Si la respuesta seguira siendo lista simple, simplificar el frontend.
  4. Ajustar el estado para consumir el contrato correcto.
- Validacion:
  - El boton siguiente funciona o se desactiva correctamente segun el contrato elegido.
  - La pagina actual coincide con los datos devueltos por la API.
- Resultado esperado: frontend y backend comparten el mismo modelo de paginacion.

---

## Tarea 6: Unificar la clase `Meta` del modelo `ListaProducto`

- Objetivo: conservar toda la configuracion del modelo en una sola definicion valida.
- Archivos involucrados: `BACKEND/inventario/models.py`.
- Problema a resolver: hay dos clases `Meta` y la segunda sobrescribe la primera.
- Pasos:
  1. Unificar `verbose_name`, `verbose_name_plural` y `ordering` en una sola clase `Meta`.
  2. Verificar que no se pierdan atributos por sobrescritura.
- Validacion:
  - El admin refleja los nombres personalizados.
  - El ordenamiento por fecha sigue activo.
- Resultado esperado: modelo limpio y sin definiciones duplicadas.

---

## Tarea 7: Limpiar la configuracion de CORS

- Objetivo: eliminar configuracion confusa y dejar una politica clara.
- Archivos involucrados: `BACKEND/inventario_api/settings.py`.
- Problema a resolver: existe una lista suelta que no afecta la configuracion real.
- Pasos:
  1. Elegir entre CORS abierto para desarrollo o whitelist de dominios.
  2. Usar la variable correcta segun la politica elegida.
  3. Eliminar lineas sueltas que no tengan efecto.
- Validacion:
  - La config de CORS queda explicita.
  - El frontend puede consumir la API sin ambiguedad.
- Resultado esperado: configuracion clara y mantenible.

---

## Cierre de cada tarea

Para dar cada tarea por terminada, verificar lo siguiente:

- El codigo corre sin errores de sintaxis.
- La ruta o flujo corregido responde como se espera.
- El comportamiento nuevo no rompe los flujos anteriores.
- Si hay tests disponibles, agregarlos o actualizarlos.

## Prioridad final recomendada

1. Ruta frontend/backend.
2. Seguridad y autenticacion.
3. Modulo `Ticket`.
4. Paginacion.
5. Limpieza de modelo y configuracion.

## Resultado esperado del plan

- La app principal queda estable.
- La API queda protegida.
- La autenticacion deja de ser decorativa.
- La documentacion tecnica se puede usar como guia real de trabajo.
