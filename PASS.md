# PASS.md - Documentación de Tests Pasados (TDD)

## 📊 RESUMEN GENERAL

**Fases Completadas:** 3-4 de 11
**Total de Tests:** 33
**Tasa de Éxito:** 100% (33/33 PASANDO)
**Cobertura:** 81% (inventario app)
**Metodología:** TDD (Test-Driven Development)

---

## FASE 3: TESTS DE MODELS (17 Tests)

### Contexto
Los tests de models verifican que el modelo `ListaProducto` funciona correctamente en la capa de base de datos. Cada test sigue TDD: test primero → debe fallar → código para pasar → verify.

**Archivo:** `/BACKEND/inventario/test_models.py`
**Clase:** `TestListaProductoModel`
**Fixture Usada:** `ListaProductoFactory`

---

### TEST 1: Crear Producto Válido ✅
**Nombre:** `test_crear_producto_valido`
**Objetivo:** Verificar que se puede crear un producto con datos válidos
**Intención:** Garantizar que el ORM de Django persiste correctamente en la BD
**Pasos de Ejecución:**
1. Crear instancia de `ListaProducto` con: nombre, descripción, cantidad, precio
2. Verificar que fue guardado en BD (tiene ID autogenerado)
3. Contar registros en BD

**Código del Test:**
```python
def test_crear_producto_valido(self):
    producto = ListaProducto.objects.create(
        nombre='Gominolas',
        descripcion='Gominolas de frutas',
        cantidad=100,
        precio=Decimal('9.99')
    )
    assert producto.id is not None
    assert producto.nombre == 'Gominolas'
    assert ListaProducto.objects.count() == 1
```

**Por Qué Pasó:**
- Django ORM funcionó correctamente
- Campo `id` se auto-generó como BigAutoField
- Los datos se persistieron en SQLite

---

### TEST 2: String Representation ✅
**Nombre:** `test_str_representation`
**Objetivo:** Verificar que `__str__()` retorna el nombre del producto
**Intención:** Garantizar que en el admin panel y logs se vea legible
**Pasos de Ejecución:**
1. Crear producto con `ListaProductoFactory(nombre='Caramelos Mexicanos')`
2. Convertir a string con `str(producto)`
3. Verificar que coincide con el nombre

**Código del Test:**
```python
def test_str_representation(self):
    producto = ListaProductoFactory(nombre='Caramelos Mexicanos')
    assert str(producto) == 'Caramelos Mexicanos'
```

**Por Qué Pasó:**
- El método `__str__()` en models.py retorna `self.nombre`
- Factory generó correctamente el nombre especificado

---

### TEST 3: Nombre Max Length ✅
**Nombre:** `test_nombre_max_length`
**Objetivo:** Validar que CharField con max_length=150 rechaza strings más largos
**Intención:** Proteger la BD de datos que exceden la capacidad del campo
**Pasos de Ejecución:**
1. Crear string de 151 caracteres (excede límite de 150)
2. Intentar validar con `full_clean()`
3. Verificar que lanza `ValidationError`

**Código del Test:**
```python
def test_nombre_max_length(self):
    nombre_largo = 'x' * 151
    producto = ListaProducto(nombre=nombre_largo, precio=Decimal('5.99'))
    with pytest.raises(ValidationError):
        producto.full_clean()
```

**Por Qué Pasó:**
- Django CharField valida max_length en `full_clean()`
- Validador incorporado detectó 151 > 150
- Lanzó `ValidationError` como se esperaba

---

### TEST 4: Cantidad Default ✅
**Nombre:** `test_cantidad_default_zero`
**Objetivo:** Verificar que cantidad tiene default=0
**Intención:** Permitir crear productos sin especificar cantidad inicial
**Pasos de Ejecución:**
1. Crear producto sin proporcionar cantidad
2. Guardar en BD
3. Verificar que cantidad==0

**Código del Test:**
```python
def test_cantidad_default_zero(self):
    producto = ListaProducto.objects.create(
        nombre='Producto sin cantidad',
        precio=Decimal('5.99')
    )
    assert producto.cantidad == 0
```

**Por Qué Pasó:**
- Campo `cantidad = IntegerField(default=0)`
- Django aplicó el default al crear sin proporcionar valor
- BD guardó 0 automáticamente

---

### TEST 5: Auto Timestamp ✅
**Nombre:** `test_fecha_auto_now_add`
**Objetivo:** Verificar que fecha_de_registro se genera automáticamente
**Intención:** Registrar cuándo se creó cada producto sin que usuario lo especifique
**Pasos de Ejecución:**
1. Capturar timestamp ANTES de crear producto
2. Crear producto con Factory (sin fecha)
3. Capturar timestamp DESPUÉS
4. Verificar que fecha_de_registro está entre antes y después

**Código del Test:**
```python
def test_fecha_auto_now_add(self):
    import datetime
    antes = datetime.datetime.now(tz=datetime.timezone.utc)
    producto = ListaProductoFactory()
    despues = datetime.datetime.now(tz=datetime.timezone.utc)
    assert antes <= producto.fecha_de_registro <= despues
```

**Por Qué Pasó:**
- Campo `fecha_de_registro = DateTimeField(auto_now_add=True)`
- Django automáticamente seteó timestamp al crear
- Timestamp estaba dentro del rango esperado

---

### TEST 6: Ordenamiento por Fecha ✅
**Nombre:** `test_ordenamiento_por_fecha`
**Objetivo:** Verificar que QuerySet se ordena automáticamente por fecha
**Intención:** Garantizar que `ListaProducto.objects.all()` retorna productos en orden cronológico
**Pasos de Ejecución:**
1. Crear 3 productos con delays pequeños
2. Obtener QuerySet sin especificar order
3. Verificar que orden es: producto1, producto2, producto3

**Código del Test:**
```python
def test_ordenamiento_por_fecha(self):
    import time
    producto1 = ListaProductoFactory(nombre='Primero')
    time.sleep(0.1)
    producto2 = ListaProductoFactory(nombre='Segundo')
    time.sleep(0.1)
    producto3 = ListaProductoFactory(nombre='Tercero')
    
    productos = ListaProducto.objects.all()
    assert list(productos) == [producto1, producto2, producto3]
```

**Por Qué Pasó:**
- Meta class especifica `ordering = ['fecha_de_registro']`
- Django aplica orden automáticamente en toda query
- Productos se retornaron en orden creciente de fecha

---

### TEST 7: Descripción Opcional ✅
**Nombre:** `test_descripcion_opcional`
**Objetivo:** Verificar que descripción puede ser NULL
**Intención:** Permitir productos sin descripción detallada
**Pasos de Ejecución:**
1. Crear producto sin proporcionar descripción
2. Guardar en BD
3. Verificar que descripción es None

**Código del Test:**
```python
def test_descripcion_opcional(self):
    producto = ListaProducto.objects.create(
        nombre='Sin descripción',
        precio=Decimal('3.99')
    )
    assert producto.descripcion is None
    assert producto.pk is not None
```

**Por Qué Pasó:**
- Campo `descripcion = TextField(blank=True, null=True)`
- Django permitió NULL en la BD
- Campo se quedó None como se esperaba

---

### TEST 8: Precisión Decimal ✅
**Nombre:** `test_precio_decimal_precision`
**Objetivo:** Verificar que precio mantiene exactitud de 2 decimales
**Intención:** Evitar errores de redondeo en operaciones monetarias
**Pasos de Ejecución:**
1. Crear producto con `Decimal('9.99')`
2. Refrescar desde BD
3. Verificar que valor es exacto 9.99

**Código del Test:**
```python
def test_precio_decimal_precision(self):
    producto = ListaProductoFactory(precio=Decimal('9.99'))
    producto.refresh_from_db()
    assert producto.precio == Decimal('9.99')
    assert str(producto.precio) == '9.99'
```

**Por Qué Pasó:**
- Campo `precio = DecimalField(max_digits=10, decimal_places=2)`
- Decimal de Python mantiene precisión exacta
- BD SQLite guardó valor sin redondeo

---

### TEST 9: Filtrar por Nombre ✅
**Nombre:** `test_filtrar_por_nombre`
**Objetivo:** Verificar que puedo filtrar productos por nombre
**Intención:** Implementar búsqueda de productos en la API
**Pasos de Ejecución:**
1. Crear 3 productos: 2 "Chocolate", 1 "Caramelo"
2. Filtrar `ListaProducto.objects.filter(nombre='Chocolate')`
3. Verificar que count() == 2

**Código del Test:**
```python
def test_filtrar_por_nombre(self):
    ListaProductoFactory(nombre='Chocolate')
    ListaProductoFactory(nombre='Caramelo')
    ListaProductoFactory(nombre='Chocolate')
    
    chocolates = ListaProducto.objects.filter(nombre='Chocolate')
    assert chocolates.count() == 2
```

**Por Qué Pasó:**
- Django ORM soporta filtros natively
- Base de datos retornó coincidencias correctas
- Count retornó 2 exactamente

---

### TEST 10: Actualizar Producto ✅
**Nombre:** `test_actualizar_producto`
**Objetivo:** Verificar que puedo modificar producto existente
**Intención:** Implementar endpoint PUT en API
**Pasos de Ejecución:**
1. Crear producto con Factory
2. Cambiar nombre y precio
3. Guardar con `.save()`
4. Refrescar desde BD
5. Verificar cambios persisten

**Código del Test:**
```python
def test_actualizar_producto(self):
    producto = ListaProductoFactory(nombre='Original', precio=Decimal('5.99'))
    producto.nombre = 'Actualizado'
    producto.precio = Decimal('7.99')
    producto.save()
    
    producto.refresh_from_db()
    assert producto.nombre == 'Actualizado'
    assert producto.precio == Decimal('7.99')
```

**Por Qué Pasó:**
- Django ORM permitió modificación de campos
- `.save()` hizo UPDATE en BD
- `.refresh_from_db()` confirmó cambios persistidos

---

### TEST 11: Eliminar Producto ✅
**Nombre:** `test_eliminar_producto`
**Objetivo:** Verificar que puedo borrar un producto
**Intención:** Implementar endpoint DELETE en API
**Pasos de Ejecución:**
1. Crear producto
2. Guardar su ID
3. Eliminar con `.delete()`
4. Verificar que no existe más en BD

**Código del Test:**
```python
def test_eliminar_producto(self):
    producto = ListaProductoFactory()
    producto_id = producto.id
    
    producto.delete()
    
    assert not ListaProducto.objects.filter(id=producto_id).exists()
```

**Por Qué Pasó:**
- Django ORM ejecutó DELETE en BD
- Registro ya no existe en table
- Query retornó False (no encontrado)

---

### TEST 12: Crear Múltiples Productos ✅
**Nombre:** `test_crear_multiples_productos`
**Objetivo:** Verificar que puedo crear varios productos
**Intención:** Garantizar comportamiento correcto en endpoints con múltiples inserciones
**Pasos de Ejecución:**
1. Crear lista de 5 productos con Factory
2. Verificar count() == 5
3. Verificar que todos tienen ID

**Código del Test:**
```python
def test_crear_multiples_productos(self):
    productos = [
        ListaProductoFactory(nombre=f'Producto {i}')
        for i in range(5)
    ]
    
    assert ListaProducto.objects.count() == 5
    assert all(p.id is not None for p in productos)
```

**Por Qué Pasó:**
- Factory creó 5 instancias independientes
- Django guardó todas en BD
- Cada una recibió ID único autogenerado

---

### TEST 13: Nombre Requerido ✅
**Nombre:** `test_nombre_requerido`
**Objetivo:** Verificar que nombre es obligatorio
**Intención:** Proteger integridad de datos (no permitir productos sin nombre)
**Pasos de Ejecución:**
1. Crear instancia sin nombre
2. Llamar `full_clean()`
3. Verificar que lanza ValidationError

**Código del Test:**
```python
def test_nombre_requerido(self):
    producto = ListaProducto(precio=Decimal('5.99'))
    with pytest.raises(ValidationError):
        producto.full_clean()
```

**Por Qué Pasó:**
- Campo `nombre` no tiene `null=True`, `blank=True`
- Django validador detectó falta de valor
- Lanzó ValidationError

---

### TEST 14: Precio Requerido ✅
**Nombre:** `test_precio_requerido`
**Objetivo:** Verificar que precio es obligatorio
**Intención:** Proteger que cada producto tenga un precio válido
**Pasos de Ejecución:**
1. Crear instancia con nombre pero sin precio
2. Llamar `full_clean()`
3. Verificar ValidationError

**Código del Test:**
```python
def test_precio_requerido(self):
    producto = ListaProducto(nombre='Sin precio')
    with pytest.raises(ValidationError):
        producto.full_clean()
```

**Por Qué Pasó:**
- Campo `precio` no tiene `null=True`
- Django requiere valor para DecimalField
- ValidationError lanzado correctamente

---

### TEST 15: Contar Productos ✅
**Nombre:** `test_contar_productos`
**Objetivo:** Verificar que `.count()` funciona correctamente
**Intención:** Implementar endpoint que retorna total de productos
**Pasos de Ejecución:**
1. Crear 3 productos
2. Llamar `ListaProducto.objects.count()`
3. Verificar que retorna 3

**Código del Test:**
```python
def test_contar_productos(self):
    for _ in range(3):
        ListaProductoFactory()
    
    assert ListaProducto.objects.count() == 3
```

**Por Qué Pasó:**
- Django ORM implementa `.count()` con SQL COUNT(*)
- BD retornó 3
- Valor coincidió exactamente

---

### TEST 16: Obtener por ID ✅
**Nombre:** `test_obtener_por_id`
**Objetivo:** Verificar que puedo obtener producto por su ID
**Intención:** Implementar endpoint GET /api/v1/tienda/<id>
**Pasos de Ejecución:**
1. Crear producto
2. Obtener con `ListaProducto.objects.get(id=...)`
3. Verificar que nombre coincide

**Código del Test:**
```python
def test_obtener_por_id(self):
    producto = ListaProductoFactory()
    
    recuperado = ListaProducto.objects.get(id=producto.id)
    assert recuperado.nombre == producto.nombre
```

**Por Qué Pasó:**
- Django `.get()` ejecutó SELECT WHERE id=...
- BD retornó exactamente un registro
- Datos coincidieron

---

### TEST 17: Obtener Inexistente Lanza Error ✅
**Nombre:** `test_obtener_inexistente_raises`
**Objetivo:** Verificar que `.get()` lanza DoesNotExist cuando ID no existe
**Intención:** Manejo correcto de errores en API (retornar 404)
**Pasos de Ejecución:**
1. Intentar obtener producto con ID=999 (no existe)
2. Verificar que lanza `ListaProducto.DoesNotExist`

**Código del Test:**
```python
def test_obtener_inexistente_raises(self):
    from django.core.exceptions import ObjectDoesNotExist
    
    with pytest.raises(ListaProducto.DoesNotExist):
        ListaProducto.objects.get(id=999)
```

**Por Qué Pasó:**
- Django `.get()` no encontró registro
- Lanzó excepción DoesNotExist (derivada de ObjectDoesNotExist)
- Pytest atrapó excepción esperada

---

## RESUMEN FASE 3

| # | Test | Objetivo | Estado |
|---|------|----------|--------|
| 1 | Create Válido | Crear y persistir | ✅ |
| 2 | __str__ | Representación legible | ✅ |
| 3 | Max Length | Validar límites | ✅ |
| 4 | Default | Valores por defecto | ✅ |
| 5 | Auto Timestamp | Timestamp automático | ✅ |
| 6 | Orden | Ordenamiento automático | ✅ |
| 7 | Nullable | Campos opcionales | ✅ |
| 8 | Decimal | Precisión monetaria | ✅ |
| 9 | Filter | Búsqueda/filtrado | ✅ |
| 10 | Update | Actualización | ✅ |
| 11 | Delete | Eliminación | ✅ |
| 12 | Bulk Create | Múltiples inserciones | ✅ |
| 13 | Required | Campos obligatorios | ✅ |
| 14 | Required | Más campos obligatorios | ✅ |
| 15 | Count | Contar registros | ✅ |
| 16 | Get by ID | Obtener por identificador | ✅ |
| 17 | Get Error | Manejo de errores | ✅ |

**Total:** 17/17 ✅ **Tiempo:** 13.43s **Cobertura:** 81%

---

## FASE 4: TESTS DE SERIALIZERS (16 Tests)

### Contexto
Los tests de serializers verifican que `UserSerializersProd` convierte correctamente entre Python objects ↔ JSON. Estos tests son críticos para la API REST.

**Archivo:** `/BACKEND/inventario/test_serializers.py`
**Clase:** `TestUserSerializersProd`
**Modelo:** `ListaProducto`
**Fixture Usada:** `ListaProductoFactory`

---

### TEST 1: Fields Correctos ✅
**Nombre:** `test_serializer_fields`
**Objetivo:** Verificar que serializer expone campos correctos
**Intención:** Asegurar que API solo retorna campos configurados
**Pasos de Ejecución:**
1. Crear instancia de serializer sin data
2. Obtener campos con `.fields.keys()`
3. Verificar que coinciden: id, nombre, descripcion, precio, cantidad, fecha_de_registro

**Código del Test:**
```python
def test_serializer_fields(self):
    serializer = UserSerializersProd()
    expected_fields = {'id', 'nombre', 'descripcion', 'precio', 'cantidad', 'fecha_de_registro'}
    actual_fields = set(serializer.fields.keys())
    assert actual_fields == expected_fields
```

**Por Qué Pasó:**
- Meta class especifica `fields = ['id', 'nombre', ...]`
- Django REST Framework leyó correctamente
- Campos coincidieron exactamente

---

### TEST 2: Serializar Producto Válido ✅
**Nombre:** `test_serializar_producto_valido`
**Objetivo:** Verificar que puedo serializar un producto a JSON
**Intención:** Verificar que objeto Python se convierte correctamente a dict
**Pasos de Ejecución:**
1. Crear producto con Factory
2. Pasarlo a serializer
3. Acceder `.data` (dict con valores)
4. Verificar que datos coinciden

**Código del Test:**
```python
def test_serializar_producto_valido(self):
    producto = ListaProductoFactory()
    serializer = UserSerializersProd(producto)
    
    assert serializer.data['nombre'] == producto.nombre
    assert serializer.data['descripcion'] == producto.descripcion
    assert serializer.data['id'] == producto.id
```

**Por Qué Pasó:**
- ModelSerializer leyó campos del modelo
- Convirtió valores a tipos JSON-compatibles
- Datos en dict coincidieron con objeto

---

### TEST 3: Nombre Requerido ✅
**Nombre:** `test_nombre_requerido`
**Objetivo:** Verificar que nombre es requerido en validación
**Intención:** API rechaza POST/PUT sin nombre
**Pasos de Ejecución:**
1. Crear dict sin 'nombre'
2. Pasar a serializer con `data=...`
3. Llamar `.is_valid()`
4. Verificar que `.errors` contiene 'nombre'

**Código del Test:**
```python
def test_nombre_requerido(self):
    data = {
        'descripcion': 'Sin nombre',
        'precio': '5.99',
        'cantidad': 10
    }
    serializer = UserSerializersProd(data=data)
    assert not serializer.is_valid()
    assert 'nombre' in serializer.errors
```

**Por Qué Pasó:**
- Campo `nombre` es requerido (no tiene `required=False`)
- Serializer detectó falta de valor
- `.errors` contiene clave 'nombre'

---

### TEST 4: Max Length Validación ✅
**Nombre:** `test_nombre_max_length_constraint`
**Objetivo:** Verificar que serializer rechaza nombres >150 chars
**Intención:** Proteger validación antes de guardar en BD
**Pasos de Ejecución:**
1. Crear dict con nombre de 151 caracteres
2. Pasar a serializer
3. Llamar `.is_valid()`
4. Verificar que is_valid() == False

**Código del Test:**
```python
def test_nombre_max_length_constraint(self):
    data = {
        'nombre': 'x' * 151,
        'precio': '5.99'
    }
    serializer = UserSerializersProd(data=data)
    assert not serializer.is_valid()
    assert 'nombre' in serializer.errors
```

**Por Qué Pasó:**
- CharField valida max_length en serializer
- 151 > 150 fue detectado
- Validación falló correctamente

---

### TEST 5: Precisión Decimal en Serialización ✅
**Nombre:** `test_precio_decimal_precision_serialization`
**Objetivo:** Verificar que precio se serializa con 2 decimales
**Intención:** API retorna precios correctamente formateados en JSON
**Pasos de Ejecución:**
1. Crear producto con `Decimal('9.99')`
2. Serializar
3. Verificar que `.data['precio']` es string "9.99"

**Código del Test:**
```python
def test_precio_decimal_precision_serialization(self):
    producto = ListaProductoFactory(precio=Decimal('9.99'))
    serializer = UserSerializersProd(producto)
    
    assert isinstance(serializer.data['precio'], str)
    assert serializer.data['precio'] == '9.99'
```

**Por Qué Pasó:**
- Django REST Framework convierte Decimal a string
- Precision se mantiene (9.99)
- Tipo es string (compatible con JSON)

---

### TEST 6: Descripción Opcional en Serialización ✅
**Nombre:** `test_descripcion_null_blank`
**Objetivo:** Verificar que descripción puede omitirse en POST/PUT
**Intención:** API permite crear productos sin descripción
**Pasos de Ejecución:**
1. Crear dict sin 'descripcion'
2. Pasar a serializer
3. Llamar `.is_valid()`
4. Verificar que is_valid() == True

**Código del Test:**
```python
def test_descripcion_null_blank(self):
    data = {
        'nombre': 'Sin descripción',
        'precio': '5.99'
    }
    serializer = UserSerializersProd(data=data)
    assert serializer.is_valid()
```

**Por Qué Pasó:**
- Campo `descripcion` tiene `required=False` (porque `blank=True` en modelo)
- Serializer permitió omisión
- Validación pasó

---

### TEST 7a: ID es Read-Only ✅
**Nombre:** `test_id_readonly`
**Objetivo:** Verificar que no se puede cambiar ID con PUT
**Intención:** Proteger ID de cambios accidentales
**Pasos de Ejecución:**
1. Crear producto con ID=1
2. Intentar actualizar con data que dice id=999
3. Guardar
4. Verificar que ID sigue siendo 1

**Código del Test:**
```python
def test_id_readonly(self):
    producto = ListaProductoFactory(id=1)
    data = {
        'nombre': 'Producto',
        'precio': '5.99',
        'id': 999  # Intentar cambiar
    }
    serializer = UserSerializersProd(producto, data=data, partial=True)
    serializer.is_valid()
    serializer.save()
    
    producto.refresh_from_db()
    assert producto.id == 1  # No cambió
```

**Por Qué Pasó:**
- ModelSerializer detecta que `id` es pk
- Automáticamente lo marca como read_only
- Intento de cambio fue ignorado

---

### TEST 7b: Fecha es Read-Only ✅
**Nombre:** `test_fecha_registro_readonly`
**Objetivo:** Verificar que fecha_de_registro no puede ser modificada
**Intención:** Proteger timestamp de creación
**Pasos de Ejecución:**
1. Crear producto con fecha original
2. Intentar actualizar con fecha diferente
3. Guardar
4. Verificar que fecha no cambió

**Código del Test:**
```python
def test_fecha_registro_readonly(self):
    import datetime
    producto = ListaProductoFactory()
    original_fecha = producto.fecha_de_registro
    
    data = {
        'nombre': 'Actualizado',
        'precio': '5.99',
        'fecha_de_registro': '2020-01-01T00:00:00Z'  # Intentar cambiar
    }
    serializer = UserSerializersProd(producto, data=data, partial=True)
    serializer.is_valid()
    serializer.save()
    
    producto.refresh_from_db()
    assert producto.fecha_de_registro == original_fecha  # No cambió
```

**Por Qué Pasó:**
- Campo con `auto_now_add=True` es read-only
- Serializer lo ignoró en actualización
- Fecha original se preservó

---

### TEST 8: Create (Serializer) ✅
**Nombre:** `test_serializer_create`
**Objetivo:** Verificar que `.save()` en nuevo serializer crea objeto
**Intención:** Implementar endpoint POST
**Pasos de Ejecución:**
1. Crear dict con datos válidos
2. Pasar a serializer
3. Validar con `.is_valid()`
4. Guardar con `.save()`
5. Verificar que objeto existe en BD

**Código del Test:**
```python
def test_serializer_create(self):
    data = {
        'nombre': 'Nuevo Producto',
        'descripcion': 'Descripción',
        'precio': '9.99',
        'cantidad': 50
    }
    serializer = UserSerializersProd(data=data)
    assert serializer.is_valid()
    
    producto = serializer.save()
    assert producto.id is not None
    assert ListaProducto.objects.filter(id=producto.id).exists()
```

**Por Qué Pasó:**
- `.save()` sin instancia ejecuta `.create()`
- Nuevo registro fue insertado
- BD asignó ID automáticamente

---

### TEST 9: Update (Serializer) ✅
**Nombre:** `test_serializer_update`
**Objetivo:** Verificar que `.save(instance=...)` actualiza existente
**Intención:** Implementar endpoint PUT
**Pasos de Ejecución:**
1. Crear producto existente
2. Crear dict con datos nuevos
3. Pasar serializer con `instance=producto`
4. Validar
5. Guardar
6. Verificar que cambios persisten

**Código del Test:**
```python
def test_serializer_update(self):
    producto = ListaProductoFactory(nombre='Viejo', precio=Decimal('5.99'))
    
    data = {
        'nombre': 'Nuevo',
        'precio': '10.99'
    }
    serializer = UserSerializersProd(producto, data=data, partial=True)
    assert serializer.is_valid()
    
    actualizado = serializer.save()
    assert actualizado.nombre == 'Nuevo'
    assert actualizado.precio == Decimal('10.99')
```

**Por Qué Pasó:**
- `.save(instance=...)` ejecuta `.update()`
- Cambios se aplicaron al objeto
- BD fue actualizada

---

### TEST 10: Cantidad en Serialización ✅
**Nombre:** `test_cantidad_default_serialization`
**Objetivo:** Verificar que cantidad se serializa correctamente
**Intención:** API retorna cantidad en respuestas
**Pasos de Ejecución:**
1. Crear producto con cantidad=0
2. Serializar
3. Verificar que `.data['cantidad']` == 0

**Código del Test:**
```python
def test_cantidad_default_serialization(self):
    producto = ListaProductoFactory(cantidad=0)
    serializer = UserSerializersProd(producto)
    
    assert serializer.data['cantidad'] == 0
```

**Por Qué Pasó:**
- Campo cantidad se incluyó en fields
- Valor 0 se serializó correctamente
- Tipo entero se preservó

---

### TEST 11: Precio Inválido ✅
**Nombre:** `test_precio_invalido`
**Objetivo:** Verificar que precio no-numérico es rechazado
**Intención:** API rechaza POST/PUT con precio "abc"
**Pasos de Ejecución:**
1. Crear dict con precio='abc'
2. Pasar a serializer
3. Validar
4. Verificar que es_valid() == False

**Código del Test:**
```python
def test_precio_invalido(self):
    data = {
        'nombre': 'Producto',
        'precio': 'abc'
    }
    serializer = UserSerializersProd(data=data)
    assert not serializer.is_valid()
    assert 'precio' in serializer.errors
```

**Por Qué Pasó:**
- DecimalField valida que sea número
- 'abc' no puede convertirse a Decimal
- Validación falló

---

### TEST 12: Precio Negativo ✅
**Nombre:** `test_precio_negativo`
**Objetivo:** Documentar comportamiento actual con precios negativos
**Intención:** Actualmente se permite (pero podría validarse)
**Pasos de Ejecución:**
1. Crear dict con precio='-5.99'
2. Pasar a serializer
3. Validar
4. Verificar que es_valid() == True (hoy se permite)

**Código del Test:**
```python
def test_precio_negativo(self):
    data = {
        'nombre': 'Producto',
        'precio': '-5.99'
    }
    serializer = UserSerializersProd(data=data)
    assert serializer.is_valid()
```

**Por Qué Pasó:**
- DecimalField actualmente acepta negativos
- No hay validador MinValueValidator
- Documentar comportamiento actual

---

### TEST 13: Múltiples Errores ✅
**Nombre:** `test_multiples_errores_validacion`
**Objetivo:** Verificar que múltiples errores se retornan juntos
**Intención:** API retorna todos los errores en una respuesta
**Pasos de Ejecución:**
1. Crear dict con nombre vacío Y precio inválido
2. Pasar a serializer
3. Validar
4. Verificar que ambos errores están en `.errors`

**Código del Test:**
```python
def test_multiples_errores_validacion(self):
    data = {
        'nombre': '',  # Error: requerido y vacío
        'precio': 'abc'  # Error: no numérico
    }
    serializer = UserSerializersProd(data=data)
    assert not serializer.is_valid()
    assert 'nombre' in serializer.errors
    assert 'precio' in serializer.errors
```

**Por Qué Pasó:**
- Serializer validó todos los campos
- Ambos errores fueron detectados
- `.errors` es dict con ambas claves

---

### TEST 14: Actualización Completa ✅
**Nombre:** `test_full_update_todos_campos`
**Objetivo:** Verificar que puedo actualizar todos los campos simultáneamente
**Intención:** Implementar PUT que actualiza múltiples campos
**Pasos de Ejecución:**
1. Crear producto
2. Crear dict con todos los campos nuevos
3. Actualizar via serializer
4. Verificar que todos cambiaron

**Código del Test:**
```python
def test_full_update_todos_campos(self):
    producto = ListaProductoFactory()
    
    data = {
        'nombre': 'Nuevo Nombre',
        'descripcion': 'Nueva Descripción',
        'precio': '99.99',
        'cantidad': 999
    }
    serializer = UserSerializersProd(producto, data=data)
    assert serializer.is_valid()
    
    actualizado = serializer.save()
    assert actualizado.nombre == 'Nuevo Nombre'
    assert actualizado.descripcion == 'Nueva Descripción'
    assert actualizado.precio == Decimal('99.99')
    assert actualizado.cantidad == 999
```

**Por Qué Pasó:**
- `.update()` aplicó todos los cambios
- BD persistió cambios
- Valores coincidieron exactamente

---

### TEST 15: Serializar Múltiples ✅
**Nombre:** `test_serializar_multiples_productos`
**Objetivo:** Verificar que puedo serializar lista de productos con many=True
**Intención:** Implementar endpoint GET /api/v1/tienda/ (lista)
**Pasos de Ejecución:**
1. Crear 3 productos
2. Pasar list a serializer con `many=True`
3. Verificar que `.data` es list con 3 items
4. Verificar que cada item tiene 'nombre'

**Código del Test:**
```python
def test_serializar_multiples_productos(self):
    productos = [ListaProductoFactory() for _ in range(3)]
    
    serializer = UserSerializersProd(productos, many=True)
    assert len(serializer.data) == 3
    assert all('nombre' in p for p in serializer.data)
```

**Por Qué Pasó:**
- `many=True` iteró sobre lista
- Cada item fue serializado
- Resultado es list de dicts

---

## RESUMEN FASE 4

| # | Test | Objetivo | Estado |
|---|------|----------|--------|
| 1 | Fields | Campos correctos | ✅ |
| 2 | Serialize | Objeto → JSON | ✅ |
| 3 | Required | Campo obligatorio | ✅ |
| 4 | Max Length | Validar límite | ✅ |
| 5 | Decimal | Precisión exacta | ✅ |
| 6 | Optional | Campo opcional | ✅ |
| 7a | Read-Only ID | Proteger ID | ✅ |
| 7b | Read-Only Fecha | Proteger timestamp | ✅ |
| 8 | Create | INSERT via serializer | ✅ |
| 9 | Update | UPDATE via serializer | ✅ |
| 10 | Integer | Cantidad correcta | ✅ |
| 11 | Invalid | Rechazar inválido | ✅ |
| 12 | Negative | Documentar negativo | ✅ |
| 13 | Multi-Error | Múltiples errores | ✅ |
| 14 | Full Update | Todos los campos | ✅ |
| 15 | Many | Serializar lista | ✅ |

**Total:** 16/16 ✅ **Tiempo:** 13.41s **Cobertura:** +9 líneas

---

## 📊 ESTADÍSTICAS GLOBALES

```
✅ FASE 3 (Models):     17 tests ✅
✅ FASE 4 (Serializers): 16 tests ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   TOTAL ACTUAL:        33 tests ✅

⏳ FASES PENDIENTES:
🔄 FASE 5 (Views GET):  ~10 tests
🔄 FASE 6 (Views POST): ~8 tests
🔄 FASE 7 (Views PUT):  ~6 tests
🔄 FASE 8 (Views DELETE): ~5 tests
🔄 FASE 9 (Validations): ~8 tests
🔄 FASE 10 (Integration): ~2 tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ESPERADO AL FINAL:   ~80 tests
```

**Cobertura Actual:** 81% (inventario app)
**Cobertura Esperada Final:** 85%+

---

## 🎯 KEY LEARNINGS

### Tests de Models
- Django ORM es robusto - validación automática de fields
- Factory pattern acelera creación de data de prueba
- `full_clean()` es crucial para validación antes de BD

### Tests de Serializers
- Serializers actúan como "API gateway" para validación
- Read-only fields se protegen automáticamente
- `many=True` es elegante para listas

### TDD Benefits Observados
1. Tests guiaron el diseño de código
2. Bugs potenciales se detectaron antes de implementar vistas
3. Código es más confiable desde el inicio
4. Documentación ejecutable (los tests)

---

## 📝 SIGUIENTES PASOS

Próxima FASE 5 cubrirá:
- ✅ Testear endpoint GET /api/v1/tienda/
- ✅ Testear endpoint GET /api/v1/tienda/<id>/
- ✅ Edge cases y errores HTTP (404, 400, etc.)
- ✅ Response format validation
- ✅ Status codes correctos

**Continuar con:** `python -m pytest inventario/ -v --cov`
