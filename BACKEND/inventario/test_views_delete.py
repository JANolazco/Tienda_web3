import pytest
from rest_framework.test import APIClient
from rest_framework import status
from inventario.models import ListaProducto
from inventario.factories import ListaProductoFactory


@pytest.mark.integration
class TestTiendaApiViewsDELETE:
    """Tests para endpoint DELETE"""

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.mark.django_db
    def test_delete_success(self, client):
        """TEST 1: DELETE elimina producto exitosamente"""
        producto = ListaProductoFactory()
        producto_id = producto.id

        response = client.delete(f'/api/v1/tienda/{producto_id}')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ListaProducto.objects.filter(id=producto_id).exists()

    @pytest.mark.django_db
    def test_delete_nonexistent(self, client):
        """TEST 2: DELETE en inexistente retorna 404"""
        response = client.delete('/api/v1/tienda/999')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_delete_no_content_body(self, client):
        """TEST 3: DELETE retorna 204 sin contenido"""
        producto = ListaProductoFactory()

        response = client.delete(f'/api/v1/tienda/{producto.id}')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.content == b''

    @pytest.mark.django_db
    def test_delete_multiple(self, client):
        """TEST 4: Eliminar múltiples productos uno por uno"""
        productos = [ListaProductoFactory() for _ in range(3)]

        for producto in productos:
            response = client.delete(f'/api/v1/tienda/{producto.id}')
            assert response.status_code == status.HTTP_204_NO_CONTENT

        assert ListaProducto.objects.count() == 0
