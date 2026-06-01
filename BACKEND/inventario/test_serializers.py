import pytest
from decimal import Decimal
from rest_framework.serializers import ValidationError
from inventario.serializers import UserSerializersProd
from inventario.models import ListaProducto
from inventario.factories import ListaProductoFactory


@pytest.mark.unit
class TestUserSerializersProd:
    """Tests unitarios para el serializador UserSerializersProd"""

    # TEST 1: Serializer Fields
    def test_serializer_fields(self):
        """TEST 1: Serializer expone campos correctos"""
        serializer = UserSerializersProd()
        expected_fields = {'id', 'nombre', 'descripcion', 'precio', 'cantidad', 'fecha_de_registro'}
        actual_fields = set(serializer.fields.keys())
        assert actual_fields == expected_fields

    # TEST 2: Valid Data Serialization
    @pytest.mark.django_db
    def test_serializar_producto_valido(self):
        """TEST 2: Serializar producto válido"""
        producto = ListaProductoFactory()
        serializer = UserSerializersProd(producto)

        assert serializer.data['nombre'] == producto.nombre
        assert serializer.data['descripcion'] == producto.descripcion
        assert serializer.data['id'] == producto.id

    # TEST 3: Required Fields
    def test_nombre_requerido(self):
        """TEST 3: nombre es requerido"""
        data = {
            'descripcion': 'Sin nombre',
            'precio': '5.99',
            'cantidad': 10
        }
        serializer = UserSerializersProd(data=data)
        assert not serializer.is_valid()
        assert 'nombre' in serializer.errors

    # TEST 4: Field Constraints - Max Length
    def test_nombre_max_length_constraint(self):
        """TEST 4a: nombre respeta max_length=150"""
        data = {
            'nombre': 'x' * 151,
            'precio': '5.99'
        }
        serializer = UserSerializersProd(data=data)
        assert not serializer.is_valid()
        assert 'nombre' in serializer.errors

    # TEST 5: Decimal Precision
    @pytest.mark.django_db
    def test_precio_decimal_precision_serialization(self):
        """TEST 5: precio se serializa con precisión correcta"""
        producto = ListaProductoFactory(precio=Decimal('9.99'))
        serializer = UserSerializersProd(producto)

        # Precio debe ser string con 2 decimales
        assert isinstance(serializer.data['precio'], str)
        assert serializer.data['precio'] == '9.99'

    # TEST 6: Null/Blank Handling
    def test_descripcion_null_blank(self):
        """TEST 6: descripcion puede ser null/blank"""
        data = {
            'nombre': 'Sin descripción',
            'precio': '5.99'
            # descripcion no se proporciona
        }
        serializer = UserSerializersProd(data=data)
        assert serializer.is_valid()

    # TEST 7: Read-Only Fields
    @pytest.mark.django_db
    def test_id_readonly(self):
        """TEST 7a: id es read-only"""
        producto = ListaProductoFactory(id=1)
        data = {
            'nombre': 'Producto',
            'precio': '5.99',
            'id': 999  # Intentar cambiar id
        }
        serializer = UserSerializersProd(producto, data=data, partial=True)
        serializer.is_valid()
        serializer.save()

        producto.refresh_from_db()
        assert producto.id == 1  # ID no cambió

    @pytest.mark.django_db
    def test_fecha_registro_readonly(self):
        """TEST 7b: fecha_de_registro es read-only"""
        import datetime
        producto = ListaProductoFactory()
        original_fecha = producto.fecha_de_registro

        data = {
            'nombre': 'Actualizado',
            'precio': '5.99',
            'fecha_de_registro': '2020-01-01T00:00:00Z'
        }
        serializer = UserSerializersProd(producto, data=data, partial=True)
        serializer.is_valid()
        serializer.save()

        producto.refresh_from_db()
        assert producto.fecha_de_registro == original_fecha

    # TEST 8: Create Method
    @pytest.mark.django_db
    def test_serializer_create(self):
        """TEST 8: serializer.save() crea objeto"""
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

    # TEST 9: Update Method
    @pytest.mark.django_db
    def test_serializer_update(self):
        """TEST 9: serializer.save(instance=...) actualiza"""
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

    # TEST 10: Cantidad Default
    @pytest.mark.django_db
    def test_cantidad_default_serialization(self):
        """TEST 10: cantidad se serializa correctamente"""
        producto = ListaProductoFactory(cantidad=0)
        serializer = UserSerializersProd(producto)

        assert serializer.data['cantidad'] == 0

    # TEST 11: Invalid Price
    def test_precio_invalido(self):
        """TEST 11: precio inválido rechazado"""
        data = {
            'nombre': 'Producto',
            'precio': 'abc'  # No es número
        }
        serializer = UserSerializersProd(data=data)
        assert not serializer.is_valid()
        assert 'precio' in serializer.errors

    # TEST 12: Negative Price
    def test_precio_negativo(self):
        """TEST 12: precio negativo puede ser rechazado"""
        data = {
            'nombre': 'Producto',
            'precio': '-5.99'
        }
        serializer = UserSerializersProd(data=data)
        # Django no rechaza negativo por default, pero podemos validar
        # Este test documenta el comportamiento actual
        assert serializer.is_valid()  # Por ahora es válido

    # TEST 13: Multiple Fields Validation
    @pytest.mark.django_db
    def test_multiples_errores_validacion(self):
        """TEST 13: Múltiples errores se retornan"""
        data = {
            'nombre': '',  # Requerido y vacío
            'precio': 'abc'  # Inválido
            # cantidad falta, pero tiene default
        }
        serializer = UserSerializersProd(data=data)
        assert not serializer.is_valid()
        assert 'nombre' in serializer.errors
        assert 'precio' in serializer.errors

    # TEST 14: Full Update
    @pytest.mark.django_db
    def test_full_update_todos_campos(self):
        """TEST 14: Actualizar todos los campos"""
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

    # TEST 15: List of Products
    @pytest.mark.django_db
    def test_serializar_multiples_productos(self):
        """TEST 15: Serializar lista de productos"""
        productos = [ListaProductoFactory() for _ in range(3)]

        serializer = UserSerializersProd(productos, many=True)
        assert len(serializer.data) == 3
        assert all('nombre' in p for p in serializer.data)
