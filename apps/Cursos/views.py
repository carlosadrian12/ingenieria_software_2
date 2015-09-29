from django.http import HttpResponse
from django.contrib import auth
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import Q

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from apps.usuarios.models import Usuario, Rol
from apps.Cursos.models import *
# Create your views here.

def mostrar_cursos(request):
    form_size = 'small'
    cursos = Curso.objects.all()
    print cursos
    return render(request, 'Cursos/mostrar-cursos.html', locals())

def nuevo_curso(request):
	form_size='small'
	#Revisar si entra a la pagina por post
	if request.method == 'POST':
		post_nombre = request.POST.get('nombre','')
		post_codigo = request.POST.get('nick','')
		post_seccion = request.POST.get('seccion','')
		post_inicio = request.POST.get('inicio','')
		post_dias = request.POST.get('dia','')
		post_hora = request.POST.get('horario','')
		post_costo = request.POST.get('precio','')
		post_maestro = request.POST.get('maestros','')
		#hacer el query al maestro
		maestros = Usuario.objects.get(user__username=post_maestro)
		print maestros
		#Crear el nuevo curso
		nuevoCurso =Curso(nick=post_codigo, nombre=post_nombre, maestro=maestros, Seccion=post_seccion,
        					inicio=post_inicio, dias=post_dias, costo = post_costo, hora=post_hora)
		nuevoCurso.save()

		return redirect('/inicio-administrador/')
		#si no entra en el POST se regresa el formulario al nuevo curso
	else:
		opcionesmaestro = Usuario.objects.filter(user__is_active=True, rol__id=4)
		return render(request,'Cursos/nuevo-curso.html',{'opcionesmaestro':opcionesmaestro,
														'form_size':form_size,})

def curso_alumno(request):
	cursos = Listas.objects.filter(fk_alumno__user__username=request.user.username)
	print cursos
	return render(request,'Cursos/cursos-alumno.html',locals()) 
