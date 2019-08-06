from django.contrib import admin
from .models import User, Connection, Address, Phone

admin.site.register(User)
admin.site.register(Connection)
admin.site.register(Address)
admin.site.register(Phone)
