import pytest
from django.test import Client
from rest_framework.test import APIClient
from inventario.models import ListaProducto
from decimal import Decimal


@pytest.fixture
def client():
    """Cliente HTTP regular para pruebas"""
    return Client()


@pytest.fixture
def api_client():
    """Cliente API REST para pruebas"""
    return APIClient()


@pytest.fixture
def producto_base():
    """Diccionario con datos base de un producto"""
    return {
        'nombre': 'Gominolas Mexicanas',
        'descripcion': 'Gominolas de frutas',
        'precio': Decimal('9.99'),
        'cantidad': 100
    }


@pytest.fixture
def producto_creado(db):
    """Crea y retorna un producto en la BD"""
    return ListaProducto.objects.create(
        nombre='Dulces Mexicanos',
        descripcion='Variedad de dulces',
        precio=Decimal('5.99'),
        cantidad=50
    )


@pytest.fixture
def productos_multiples(db):
    """Crea múltiples productos en la BD"""
    return [
        ListaProducto.objects.create(
            nombre=f'Producto {i}',
            descripcion=f'Descripción {i}',
            precio=Decimal(f'{i}.99'),
            cantidad=10*i
        )
        for i in range(1, 6)
    ]


@pytest.fixture
def producto_invalido():
    """Diccionario con datos inválidos"""
    return {
        'nombre': '',  # Nombre vacío
        'precio': '-5.99'  # Precio negativo
    }
