from django.contrib import admin
from apps.usuarios.models import Usuario, Rol, Pagos
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(Pagos)