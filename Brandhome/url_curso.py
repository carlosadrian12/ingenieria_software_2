from django.conf.urls import include, url
from django.contrib import admin

from apps.Cursos.views import *
from apps.usuarios.views import *

url_curso = [
    url(r'^inicio-administrador/mostrar/cursos/', mostrar_cursos),
    url(r'^cursos/nuevo-curso', nuevo_curso),
    url(r'^formato-pago/', formato_pago),
    url(r'^lista-cursos/$', lista_cursos),
    url(r'^cursos-selec/$',seleccionar_cursos),
    url(r'^cursos-alumno/$',curso_alumno),
]
