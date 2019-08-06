from django.contrib import admin
from .models import User, Connection, Address, Phone, Categoria, Inventario, Articulo, Factura, Rol, Encargado, Orden

admin.site.register(User)
admin.site.register(Connection)
admin.site.register(Address)
admin.site.register(Phone)
admin.site.register(Categoria)
admin.site.register(Inventario)
admin.site.register(Articulo)
admin.site.register(Factura)
admin.site.register(Rol)
admin.site.register(Encargado)
admin.site.register(Orden)
