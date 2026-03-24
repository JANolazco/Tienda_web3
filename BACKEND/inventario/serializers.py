from rest_framework.serializers import ModelSerializer
from .models import ListaProducto

#creando las serializacion de registro
class UserSerializersProd(ModelSerializer):
    class Meta:
        model= ListaProducto
        fields=['id','nombre','descripcion','precio']
        
