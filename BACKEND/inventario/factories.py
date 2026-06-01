import factory
from factory.django import DjangoModelFactory
from decimal import Decimal
from faker import Faker
from .models import ListaProducto

fake = Faker('es_MX')


class ListaProductoFactory(DjangoModelFactory):
    """Factory para crear instancias de ListaProducto con datos aleatorios"""

    class Meta:
        model = ListaProducto

    nombre = factory.Sequence(lambda n: f'Producto {n}')
    descripcion = factory.LazyAttribute(lambda o: fake.text(max_nb_chars=100))
    cantidad = factory.Faker('random_int', min=1, max=1000)
    precio = factory.LazyAttribute(
        lambda o: Decimal(str(round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)))
    )

    class Params:
        """Parámetros adicionales para customizar en tests"""
        with_specific_price = factory.Trait(
            precio=Decimal('9.99')
        )
        with_large_quantity = factory.Trait(
            cantidad=1000
        )
        with_name = factory.Trait(
            nombre='Dulces Mexicanos'
        )
