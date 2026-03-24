from django.db import models

# Create your models here.
class ListaProducto(models.Model):
    nombre=models.CharField(max_length=150)
    descripcion=models.TextField(blank=True, null= True)
    cantidad=models.IntegerField(default=0)
    precio=models.DecimalField(max_digits=10, decimal_places=2)
    fecha_de_registro=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    #pasos para convertir en español la apk admin
    class Meta:
        verbose_name='Lista_de_Producto'
        verbose_name_plural='Producto infos'
    
    #lo utilizo para ordenar por fecha de registro
    class Meta:
        ordering= ['fecha_de_registro']