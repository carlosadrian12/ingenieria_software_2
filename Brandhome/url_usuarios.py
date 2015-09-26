from django.conf.urls import include, url
from django.contrib import admin

from apps.usuarios.views import *

url_usuarios = [
	url(r'^$', login, name='login'),
    url(r'^login/$', login),
    url(r'^logout/$', logout, name='logout'),
	url(r'^inicio-administrador/$', inicio_admin, name='inicio_admin'),
	url(r'^inicio-alumno/$', inicio_alumno),
    url(r'^modificar-perfil/$',modificar_perfil),
    url(r'^modificar-password/$',modificar_password), 
    url(r'^registro-alumno/nuevo/$', nuevo_alumno),
    url(r'^activar_usuarios',activar_usuarios),
    url(r'^nuevo/secrearia', nueva_secretaria),
    url(r'^inicio-administrador/nuevo/maestro', nuevo_maestro),
    url(r'^activar-maestros', activar_maestros),
]
