import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status
from inventario.models import ListaProducto
from inventario.factories import ListaProductoFactory


@pytest.mark.integration
class TestTiendaApiViewsGET:
    """Tests de integración para endpoint GET"""

    @pytest.fixture
    def client(self):
        """Cliente API para tests"""
        return APIClient()

    # TEST 1: GET Lista Vacía
    @pytest.mark.django_db
    def test_get_empty_list(self, client):
        """TEST 1: GET /api/v1/tienda/ sin productos retorna lista vacía"""
        response = client.get('/api/v1/tienda/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    # TEST 2: GET Lista con Productos
    @pytest.mark.django_db
    def test_get_products_list(self, client):
        """TEST 2: GET /api/v1/tienda/ retorna todos los productos"""
        # Setup: Crear 3 productos
        producto1 = ListaProductoFactory(nombre='Producto 1', precio=Decimal('5.99'))
        producto2 = ListaProductoFactory(nombre='Producto 2', precio=Decimal('7.99'))
        producto3 = ListaProductoFactory(nombre='Producto 3', precio=Decimal('9.99'))

        # Request
        response = client.get('/api/v1/tienda/')

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert data[0]['nombre'] == 'Producto 1'
        assert data[1]['nombre'] == 'Producto 2'
        assert data[2]['nombre'] == 'Producto 3'

    # TEST 3: GET Producto por ID
    @pytest.mark.django_db
    def test_get_product_by_id(self, client):
        """TEST 3: GET /api/v1/tienda/<id> retorna producto específico"""
        # Setup
        producto = ListaProductoFactory(nombre='Dulce Especial', precio=Decimal('12.99'))

        # Request
        response = client.get(f'/api/v1/tienda/{producto.id}')

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['id'] == producto.id
        assert data['nombre'] == 'Dulce Especial'
        assert data['precio'] == '12.99'

    # TEST 4: GET Producto No Existe
    @pytest.mark.django_db
    def test_get_nonexistent_product(self, client):
        """TEST 4: GET /api/v1/tienda/999 retorna 404"""
        response = client.get('/api/v1/tienda/999')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # TEST 5: GET Response Format
    @pytest.mark.django_db
    def test_get_response_structure(self, client):
        """TEST 5: Response tiene estructura correcta"""
        producto = ListaProductoFactory()

        response = client.get(f'/api/v1/tienda/{producto.id}')
        data = response.json()

        # Verificar que contiene todos los campos
        assert 'id' in data
        assert 'nombre' in data
        assert 'descripcion' in data
        assert 'precio' in data
        assert 'cantidad' in data
        assert 'fecha_de_registro' in data

    # TEST 6: GET Tipos de Datos Correctos
    @pytest.mark.django_db
    def test_get_field_types(self, client):
        """TEST 6: Tipos de datos en response son correctos"""
        producto = ListaProductoFactory()

        response = client.get(f'/api/v1/tienda/{producto.id}')
        data = response.json()

        # Verificar tipos
        assert isinstance(data['id'], int)
        assert isinstance(data['nombre'], str)
        assert isinstance(data['descripcion'], (str, type(None)))  # Puede ser null
        assert isinstance(data['precio'], str)  # Decimal como string
        assert isinstance(data['cantidad'], int)
        assert isinstance(data['fecha_de_registro'], str)  # ISO format

    # TEST 7: GET Content-Type
    @pytest.mark.django_db
    def test_get_content_type(self, client):
        """TEST 7: Response tiene Content-Type: application/json"""
        producto = ListaProductoFactory()

        response = client.get(f'/api/v1/tienda/{producto.id}')

        assert response['Content-Type'] == 'application/json'

    # TEST 8: GET List Ordenamiento
    @pytest.mark.django_db
    def test_get_list_ordering(self, client):
        """TEST 8: GET /api/v1/tienda/ respeta ordenamiento por fecha"""
        import time

        # Crear 3 productos con pequeño delay
        p1 = ListaProductoFactory(nombre='Primero')
        time.sleep(0.05)
        p2 = ListaProductoFactory(nombre='Segundo')
        time.sleep(0.05)
        p3 = ListaProductoFactory(nombre='Tercero')

        response = client.get('/api/v1/tienda/')
        data = response.json()

        # Verificar orden
        assert data[0]['nombre'] == 'Primero'
        assert data[1]['nombre'] == 'Segundo'
        assert data[2]['nombre'] == 'Tercero'

    # TEST 9: GET ID Negativo
    @pytest.mark.django_db
    def test_get_negative_id(self, client):
        """TEST 9: GET /api/v1/tienda/-1 retorna 404"""
        response = client.get('/api/v1/tienda/-1')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # TEST 10: GET ID String
    @pytest.mark.django_db
    def test_get_string_id(self, client):
        """TEST 10: GET /api/v1/tienda/abc retorna error"""
        response = client.get('/api/v1/tienda/abc')

        # Puede ser 404 o 400 dependiendo del routing
        assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]

    # TEST 11: GET Precio Decimal
    @pytest.mark.django_db
    def test_get_precio_formato(self, client):
        """TEST 11: Precio se serializa correctamente con 2 decimales"""
        producto = ListaProductoFactory(precio=Decimal('9.99'))

        response = client.get(f'/api/v1/tienda/{producto.id}')
        data = response.json()

        assert data['precio'] == '9.99'
        assert isinstance(data['precio'], str)

    # TEST 12: GET Descripción Null
    @pytest.mark.django_db
    def test_get_null_description(self, client):
        """TEST 12: Descripción null se serializa como null"""
        producto = ListaProductoFactory(descripcion=None)

        response = client.get(f'/api/v1/tienda/{producto.id}')
        data = response.json()

        assert data['descripcion'] is None

    # TEST 13: GET Cantidad Zero
    @pytest.mark.django_db
    def test_get_zero_quantity(self, client):
        """TEST 13: Cantidad 0 se serializa correctamente"""
        producto = ListaProductoFactory(cantidad=0)

        response = client.get(f'/api/v1/tienda/{producto.id}')
        data = response.json()

        assert data['cantidad'] == 0

    # TEST 14: GET Large List
    @pytest.mark.django_db
    def test_get_large_list(self, client):
        """TEST 14: GET retorna correctamente con muchos productos"""
        # Crear 50 productos
        for i in range(50):
            ListaProductoFactory(nombre=f'Producto {i}')

        response = client.get('/api/v1/tienda/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 50

    # TEST 15: GET Response Completo
    @pytest.mark.django_db
    def test_get_complete_response(self, client):
        """TEST 15: Response completo contiene todos los datos correctamente"""
        producto = ListaProductoFactory(
            nombre='Caramelos Mexicanos',
            descripcion='Caramelos tradicionales',
            precio=Decimal('8.50'),
            cantidad=100
        )

        response = client.get(f'/api/v1/tienda/{producto.id}')
        data = response.json()

        # Verificar cada campo
        assert data['id'] == producto.id
        assert data['nombre'] == 'Caramelos Mexicanos'
        assert data['descripcion'] == 'Caramelos tradicionales'
        assert data['precio'] == '8.50'
        assert data['cantidad'] == 100
        assert data['fecha_de_registro'] is not None
