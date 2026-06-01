from django.contrib import admin
from .models import ListaProducto

@admin.register(ListaProducto)
class ListaProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'cantidad', 'fecha_de_registro')
    list_filter = ('fecha_de_registro',)
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_de_registro',)
    fieldsets = (
        ('Información del Producto', {
            'fields': ('nombre', 'descripcion', 'precio', 'cantidad')
        }),
        ('Metadata', {
            'fields': ('fecha_de_registro',),
            'classes': ('collapse',)
        }),
    )