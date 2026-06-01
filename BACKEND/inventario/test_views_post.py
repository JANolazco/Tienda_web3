import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status
from inventario.models import ListaProducto
from inventario.factories import ListaProductoFactory


@pytest.mark.integration
class TestTiendaApiViewsPOST:
    """Tests de integración para endpoint POST"""

    @pytest.fixture
    def client(self):
        return APIClient()

    # TEST 1: POST Crear Válido
    @pytest.mark.django_db
    def test_post_create_valid(self, client):
        """TEST 1: POST /api/v1/tienda/ crea producto válido"""
        data = {
            'nombre': 'Caramelos Mexicanos',
            'descripcion': 'Caramelos frescos',
            'precio': '7.99',
            'cantidad': 50
        }

        response = client.post('/api/v1/tienda/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['nombre'] == 'Caramelos Mexicanos'
        assert ListaProducto.objects.count() == 1

    # TEST 2: POST Nombre Requerido
    @pytest.mark.django_db
    def test_post_missing_nombre(self, client):
        """TEST 2: POST sin nombre retorna 400"""
        data = {
            'descripcion': 'Sin nombre',
            'precio': '5.99'
        }

        response = client.post('/api/v1/tienda/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'nombre' in response.json()

    # TEST 3: POST Precio Requerido
    @pytest.mark.django_db
    def test_post_missing_precio(self, client):
        """TEST 3: POST sin precio retorna 400"""
        data = {
            'nombre': 'Producto',
            'descripcion': 'Descripción'
        }

        response = client.post('/api/v1/tienda/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'precio' in response.json()

    # TEST 4: POST Descripción Opcional
    @pytest.mark.django_db
    def test_post_optional_descripcion(self, client):
        """TEST 4: POST sin descripción es válido"""
        data = {
            'nombre': 'Producto',
            'precio': '5.99'
        }

        response = client.post('/api/v1/tienda/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['descripcion'] is None

    # TEST 5: POST Response Contiene ID
    @pytest.mark.django_db
    def test_post_response_has_id(self, client):
        """TEST 5: Response POST incluye ID generado"""
        data = {
            'nombre': 'Producto',
            'precio': '5.99'
        }

        response = client.post('/api/v1/tienda/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.json()
        assert isinstance(response.json()['id'], int)
        assert response.json()['id'] > 0

    # TEST 6: POST Precio Inválido
    @pytest.mark.django_db
    def test_post_invalid_precio(self, client):
        """TEST 6: POST con precio inválido retorna 400"""
        data = {
            'nombre': 'Producto',
            'precio': 'abc'
        }

        response = client.post('/api/v1/tienda/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'precio' in response.json()

    # TEST 7: POST Nombre Muy Largo
    @pytest.mark.django_db
    def test_post_nombre_too_long(self, client):
        """TEST 7: POST con nombre >150 chars retorna 400"""
        data = {
            'nombre': 'x' * 151,
            'precio': '5.99'
        }

        response = client.post('/api/v1/tienda/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'nombre' in response.json()

    # TEST 8: POST Cantidad Omitida
    @pytest.mark.django_db
    def test_post_default_cantidad(self, client):
        """TEST 8: POST sin cantidad usa default=0"""
        data = {
            'nombre': 'Producto',
            'precio': '5.99'
        }

        response = client.post('/api/v1/tienda/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        producto = ListaProducto.objects.get(nombre='Producto')
        assert producto.cantidad == 0

    # TEST 9: POST Multiple Productos
    @pytest.mark.django_db
    def test_post_multiple_products(self, client):
        """TEST 9: Crear múltiples productos con POST"""
        for i in range(3):
            data = {
                'nombre': f'Producto {i}',
                'precio': f'{i}.99'
            }
            response = client.post('/api/v1/tienda/', data, format='json')
            assert response.status_code == status.HTTP_201_CREATED

        assert ListaProducto.objects.count() == 3

    # TEST 10: POST Content-Type
    @pytest.mark.django_db
    def test_post_response_content_type(self, client):
        """TEST 10: Response POST tiene Content-Type correcto"""
        data = {
            'nombre': 'Producto',
            'precio': '5.99'
        }

        response = client.post('/api/v1/tienda/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response['Content-Type'] == 'application/json'

    # TEST 11: POST Precio Negativo
    @pytest.mark.django_db
    def test_post_negative_price(self, client):
        """TEST 11: POST con precio negativo actualmente se permite"""
        data = {
            'nombre': 'Producto',
            'precio': '-5.99'
        }

        response = client.post('/api/v1/tienda/', data, format='json')

        # Actualmente se permite, pero documenta el comportamiento
        assert response.status_code == status.HTTP_201_CREATED

    # TEST 12: POST Nombre Vacío
    @pytest.mark.django_db
    def test_post_empty_nombre(self, client):
        """TEST 12: POST con nombre vacío retorna 400"""
        data = {
            'nombre': '',
            'precio': '5.99'
        }

        response = client.post('/api/v1/tienda/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # TEST 13: POST Precio Cero
    @pytest.mark.django_db
    def test_post_zero_price(self, client):
        """TEST 13: POST con precio 0.00 es válido"""
        data = {
            'nombre': 'Producto Gratis',
            'precio': '0.00'
        }

        response = client.post('/api/v1/tienda/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['precio'] == '0.00'
