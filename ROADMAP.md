# ROADMAP.md - TEMPORAL (Eliminar cuando proyecto esté completado)

## 📋 OBJETIVO FINAL
Llevar el proyecto de **7.5/10 a 8.5/10** → Portfolio profesional listo

---

## 🎯 TAREAS PENDIENTES (4-6 horas totales)

### TAREA 1: Deploy en Producción (1-2 horas)

**¿QUÉ ES?**
Actualmente el proyecto solo corre localmente. Necesita estar "vivo" en internet para que los recruiters lo vean funcionando.

**¿POR QUÉ?**
- Demuestra que funciona en producción (no solo en tu PC)
- Los recruiters hacen click en URL viva
- Diferencia entre proyecto "hobby" y "profesional"

**¿CÓMO HACERLO?**

**Para Persona:**
1. Crear cuenta en Vercel (gratis) - 5 min
2. Conectar repositorio GitHub - 5 min
3. Deployer frontend (Vercel auto-detecta Reflex)
4. Crear cuenta en Railway (gratis) - 5 min
5. Deployer backend Django - 10 min
6. Conectar URLs (frontend → backend API)
7. Probar que funciona - 10 min

**Para Agent:**
```bash
# Pasos técnicos:
1. Crear archivo vercel.json en TIENDA_FRONTED/
2. Crear archivo railway.json o configurar en Railway dashboard
3. Actualizar API_URL en frontend para producción
4. Configurar variables de entorno (.env en Railway)
5. Hacer push
6. Verificar logs de deployment
```

**Archivos a modificar:**
- `TIENDA_FRONTED/vercel.json` (crear)
- `BACKEND/railway.toml` (crear)
- `TIENDA_FRONTED/TIENDA_FRONTED/state.py` (actualizar API_URL)
- `BACKEND/inventario_api/settings.py` (agregar dominio a ALLOWED_HOSTS)

---

### TAREA 2: Mejorar UI (2-3 horas)

**¿QUÉ ES?**
Hacer que se vea profesional con colores, tipografía, espaciado.

**¿POR QUÉ?**
- Primera impresión importa MUCHO
- UI fea = "proyecto de estudiante"
- UI pulida = "desarrollador profesional"

**¿CÓMO HACERLO?**

**Para Persona:**
1. Definir color scheme (ej: azul + blanco + gris)
2. Usar iconos consistentes
3. Mejorar botones (agregar bordes redondeados, sombras)
4. Mejorar tabla (alternancia de colores, hover effects)
5. Agregar logo/branding
6. Hacer responsive (mobile-friendly)

**Para Agent:**
```python
# Ejemplos en Reflex:

# Antes:
rx.button("Nuevo Producto")

# Después:
rx.button(
    "Nuevo Producto",
    size="md",
    color_scheme="blue",
    width="200px",
    border_radius="8px",
)

# Mejorar tabla con colores:
rx.table.row(
    rx.table.cell(producto["nombre"], bg_color="#f5f5f5" if i % 2 == 0 else "white"),
    ...
)
```

**Archivos a modificar:**
- `TIENDA_FRONTED/TIENDA_FRONTED/pages/index.py` (estructura UI)
- `TIENDA_FRONTED/TIENDA_FRONTED/components/product_form.py` (formulario)
- `TIENDA_FRONTED/TIENDA_FRONTED/components/product_table.py` (tabla)
- `TIENDA_FRONTED/TIENDA_FRONTED/TIENDA_FRONTED.py` (theme global)

**Color scheme sugerido:**
```
Primary: #3B82F6 (Azul)
Secondary: #10B981 (Verde)
Error: #EF4444 (Rojo)
Background: #F9FAFB (Gris claro)
Text: #1F2937 (Gris oscuro)
```

---

### TAREA 3: Agregar Feature: Búsqueda/Filtrado (1-1.5 horas)

**¿QUÉ ES?**
Campo de búsqueda donde usuarios puedan escribir "caramelo" y ver solo productos con esa palabra.

**¿POR QUÉ?**
- Feature "wow" que muestra competencia
- Hace la app más útil
- Demuestra manejo de state + filtering

**¿CÓMO HACERLO?**

**Para Persona:**
1. Agregar input text para búsqueda en la UI
2. En el estado, agregar `busqueda: str = ""`
3. Filtrar productos mientras el usuario escribe
4. Mostrar "0 resultados" si no hay coincidencias

**Para Agent:**
```python
# En state.py:
class State(rx.State):
    # ... otros campos
    busqueda: str = ""
    
    def set_busqueda(self, value: str):
        self.busqueda = value
    
    @computed_var
    def productos_filtrados(self) -> list:
        if not self.busqueda:
            return self.productos
        busqueda_lower = self.busqueda.lower()
        return [
            p for p in self.productos 
            if busqueda_lower in p['nombre'].lower()
        ]

# En pages/index.py:
rx.input(
    placeholder="Buscar producto...",
    value=State.busqueda,
    on_change=State.set_busqueda,
    width="100%"
)

# Mostrar cantidad de resultados
rx.text(f"Encontrados: {len(State.productos_filtrados)}")
```

**Archivos a modificar:**
- `TIENDA_FRONTED/TIENDA_FRONTED/state.py` (agregar búsqueda)
- `TIENDA_FRONTED/TIENDA_FRONTED/pages/index.py` (UI de búsqueda)
- `TIENDA_FRONTED/TIENDA_FRONTED/components/product_table.py` (usar productos_filtrados)

---

## 📊 TIEMPO ESTIMADO

| Tarea | Persona | Agent | Total |
|-------|---------|-------|-------|
| Deploy | 1h | 20min | 1.5h |
| UI | 1.5h | 45min | 2h |
| Búsqueda | 45min | 30min | 1h |
| **TOTAL** | **3.25h** | **1.5h** | **~4.5h** |

---

## ✅ CRITERIOS DE ÉXITO

**Deploy:**
- ✅ Frontend corre en Vercel
- ✅ Backend corre en Railway
- ✅ URL viva funciona desde el navegador
- ✅ CRUD completo funciona remotamente

**UI:**
- ✅ Se ve profesional (no "homework")
- ✅ Colores consistentes
- ✅ Responsive en móvil
- ✅ Sin errores visuales

**Búsqueda:**
- ✅ Filtra en tiempo real
- ✅ Muestra resultado count
- ✅ Funciona en deploy

---

## 🎯 RESULTADO FINAL

Después de completar estas tareas:
- **Calificación:** 8.5/10
- **Estado:** Listo para portafolio profesional
- **Impresión:** "Desarrollador serio, no hobby"

---

## 📝 NOTAS

- Cada tarea es independiente (se pueden hacer en cualquier orden)
- Todas las tareas son completables sin cambiar tests
- Tests ya pasarán con las nuevas features
- Considerar hacer PR después de cada tarea completada
