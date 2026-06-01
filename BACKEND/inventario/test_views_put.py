import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status
from inventario.models import ListaProducto
from inventario.factories import ListaProductoFactory


@pytest.mark.integration
class TestTiendaApiViewsPUT:
    """Tests para endpoint PUT"""

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.mark.django_db
    def test_put_update_nombre(self, client):
        """TEST 1: PUT actualiza nombre"""
        producto = ListaProductoFactory(nombre='Viejo')
        data = {'nombre': 'Nuevo', 'precio': str(producto.precio)}

        response = client.put(f'/api/v1/tienda/{producto.id}', data, format='json')

        assert response.status_code == status.HTTP_200_OK
        producto.refresh_from_db()
        assert producto.nombre == 'Nuevo'

    @pytest.mark.django_db
    def test_put_update_precio(self, client):
        """TEST 2: PUT actualiza precio"""
        producto = ListaProductoFactory(precio=Decimal('5.99'))
        data = {'nombre': producto.nombre, 'precio': '10.99'}

        response = client.put(f'/api/v1/tienda/{producto.id}', data, format='json')

        assert response.status_code == status.HTTP_200_OK
        producto.refresh_from_db()
        assert producto.precio == Decimal('10.99')

    @pytest.mark.django_db
    def test_put_nonexistent(self, client):
        """TEST 3: PUT en inexistente retorna 404"""
        data = {'nombre': 'Test', 'precio': '5.99'}

        response = client.put('/api/v1/tienda/999', data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_put_invalid_precio(self, client):
        """TEST 4: PUT con precio inválido retorna 400"""
        producto = ListaProductoFactory()
        data = {'nombre': 'Test', 'precio': 'abc'}

        response = client.put(f'/api/v1/tienda/{producto.id}', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_put_all_fields(self, client):
        """TEST 5: PUT actualiza todos los campos"""
        producto = ListaProductoFactory()

        data = {
            'nombre': 'Nuevo',
            'descripcion': 'Nueva Desc',
            'precio': '99.99',
            'cantidad': 999
        }
        response = client.put(f'/api/v1/tienda/{producto.id}', data, format='json')

        assert response.status_code == status.HTTP_200_OK
        producto.refresh_from_db()
        assert producto.nombre == 'Nuevo'
        assert producto.cantidad == 999
