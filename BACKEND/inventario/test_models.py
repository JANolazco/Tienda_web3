import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from inventario.models import ListaProducto
from inventario.factories import ListaProductoFactory


@pytest.mark.unit
class TestListaProductoModel:
    """Tests unitarios para el modelo ListaProducto"""

    # TEST 1: Model Creation
    @pytest.mark.django_db
    def test_crear_producto_valido(self):
        """TEST 1: Crear ListaProducto con campos válidos"""
        # Red: Escribir test que FALLA
        producto = ListaProducto.objects.create(
            nombre='Gominolas',
            descripcion='Gominolas de frutas',
            cantidad=100,
            precio=Decimal('9.99')
        )

        # Green: Verificar que fue creado
        assert producto.id is not None
        assert producto.nombre == 'Gominolas'
        assert ListaProducto.objects.count() == 1

    # TEST 2: String Representation
    @pytest.mark.django_db
    def test_str_representation(self):
        """TEST 2: str(producto) retorna nombre"""
        producto = ListaProductoFactory(nombre='Caramelos Mexicanos')
        assert str(producto) == 'Caramelos Mexicanos'

    # TEST 3: Field Validations - Max Length
    @pytest.mark.django_db
    def test_nombre_max_length(self):
        """TEST 3a: nombre tiene max_length=150"""
        nombre_largo = 'x' * 151
        producto = ListaProducto(
            nombre=nombre_largo,
            precio=Decimal('5.99')
        )
        # Django valida en full_clean()
        with pytest.raises(ValidationError):
            producto.full_clean()

    # TEST 4: Default Values
    @pytest.mark.django_db
    def test_cantidad_default_zero(self):
        """TEST 4: cantidad default=0"""
        producto = ListaProducto.objects.create(
            nombre='Producto sin cantidad',
            precio=Decimal('5.99')
        )
        assert producto.cantidad == 0

    # TEST 5: Auto Timestamp
    @pytest.mark.django_db
    def test_fecha_auto_now_add(self):
        """TEST 5: fecha_de_registro se genera automáticamente"""
        import datetime
        antes = datetime.datetime.now(tz=datetime.timezone.utc)

        producto = ListaProductoFactory()

        despues = datetime.datetime.now(tz=datetime.timezone.utc)
        assert antes <= producto.fecha_de_registro <= despues

    # TEST 6: Ordering
    @pytest.mark.django_db
    def test_ordenamiento_por_fecha(self):
        """TEST 6: QuerySet se ordena por fecha_de_registro"""
        import time

        # Crear productos con pequeño delay
        producto1 = ListaProductoFactory(nombre='Primero')
        time.sleep(0.1)
        producto2 = ListaProductoFactory(nombre='Segundo')
        time.sleep(0.1)
        producto3 = ListaProductoFactory(nombre='Tercero')

        # Obtener en order
        productos = ListaProducto.objects.all()
        assert list(productos) == [producto1, producto2, producto3]

    # TEST 7: Null/Blank Fields
    @pytest.mark.django_db
    def test_descripcion_opcional(self):
        """TEST 7: descripcion es null=True, blank=True"""
        producto = ListaProducto.objects.create(
            nombre='Sin descripción',
            precio=Decimal('3.99')
            # descripcion no se proporciona
        )
        assert producto.descripcion is None
        assert producto.pk is not None

    # TEST 8: Decimal Precision
    @pytest.mark.django_db
    def test_precio_decimal_precision(self):
        """TEST 8: precio mantiene precisión de 2 decimales"""
        producto = ListaProductoFactory(precio=Decimal('9.99'))
        producto.refresh_from_db()

        # Verificar precisión exacta
        assert producto.precio == Decimal('9.99')
        assert str(producto.precio) == '9.99'

    # TEST 9: Queryset Filtering
    @pytest.mark.django_db
    def test_filtrar_por_nombre(self):
        """TEST 9: Puedo filtrar productos por nombre"""
        ListaProductoFactory(nombre='Chocolate')
        ListaProductoFactory(nombre='Caramelo')
        ListaProductoFactory(nombre='Chocolate')

        chocolates = ListaProducto.objects.filter(nombre='Chocolate')
        assert chocolates.count() == 2

    # TEST 10: Update
    @pytest.mark.django_db
    def test_actualizar_producto(self):
        """TEST 10: Puedo actualizar un producto"""
        producto = ListaProductoFactory(nombre='Original', precio=Decimal('5.99'))

        producto.nombre = 'Actualizado'
        producto.precio = Decimal('7.99')
        producto.save()

        producto.refresh_from_db()
        assert producto.nombre == 'Actualizado'
        assert producto.precio == Decimal('7.99')

    # TEST 11: Delete
    @pytest.mark.django_db
    def test_eliminar_producto(self):
        """TEST 11: Puedo eliminar un producto"""
        producto = ListaProductoFactory()
        producto_id = producto.id

        producto.delete()

        assert not ListaProducto.objects.filter(id=producto_id).exists()

    # TEST 12: Bulk Create
    @pytest.mark.django_db
    def test_crear_multiples_productos(self):
        """TEST 12: Puedo crear múltiples productos a la vez"""
        productos = [
            ListaProductoFactory(nombre=f'Producto {i}')
            for i in range(5)
        ]

        assert ListaProducto.objects.count() == 5
        assert all(p.id is not None for p in productos)

    # TEST 13: Required Fields
    @pytest.mark.django_db
    def test_nombre_requerido(self):
        """TEST 13: nombre es requerido"""
        # Intentar crear sin nombre debe fallar
        producto = ListaProducto(precio=Decimal('5.99'))
        with pytest.raises(ValidationError):
            producto.full_clean()

    @pytest.mark.django_db
    def test_precio_requerido(self):
        """TEST 14: precio es requerido"""
        producto = ListaProducto(nombre='Sin precio')
        with pytest.raises(ValidationError):
            producto.full_clean()

    # TEST 15: Count
    @pytest.mark.django_db
    def test_contar_productos(self):
        """TEST 15: Puedo contar productos"""
        for _ in range(3):
            ListaProductoFactory()

        assert ListaProducto.objects.count() == 3

    # TEST 16: Get by ID
    @pytest.mark.django_db
    def test_obtener_por_id(self):
        """TEST 16: Puedo obtener producto por ID"""
        producto = ListaProductoFactory()

        recuperado = ListaProducto.objects.get(id=producto.id)
        assert recuperado.nombre == producto.nombre

    # TEST 17: Get No Existe
    @pytest.mark.django_db
    def test_obtener_inexistente_raises(self):
        """TEST 17: Obtener inexistente lanza DoesNotExist"""
        from django.core.exceptions import ObjectDoesNotExist

        with pytest.raises(ListaProducto.DoesNotExist):
            ListaProducto.objects.get(id=999)
