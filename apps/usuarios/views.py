# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from apps.usuarios.models import Usuario, Rol, Pagos
from apps.Cursos.models import Curso, Listas
# Create your views here.
# las plantillas que se llamen mas de una vez es mejor ponerlas como constantes
TEMPLATE_MODIFICA_PASS = 'Usuarios/modificar-password.html'
def inicio(request):
    banner = True
    bienvenida = False
    return render(request, 'base_gral.html', locals())

def inicio_admin(request):
    #revisa que el usuario tenga permisos necesarios para ver el contenido de esta página
    if request.session['rol'] == 3:
        banner = True
        bienvenida = False

        if request.session['just_logged']:
            bienvenida = True
            request.session['just_logged'] = False
            
        return render(request, 'Usuarios/inicio_admi.html', locals())
    else:
        return redirect('error403', origen=request.path)

def inicio_alumno(request):
    #revisa que el usuario tenga permisos necesarios para ver el contenido de esta página
    if request.session['rol'] == 1:
        banner = True
        bienvenida = False

        if request.session['just_logged']:
            bienvenida = True
            request.session['just_logged'] = False
    
        return render(request, 'inicio-alumno.html', locals())
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def modificar_perfil(request):
    if request.session['rol'] >= 1: # basicamente cualquier usuario, no? e.e
        form_size = 'small'
        user_modificar = request.session['usuario']['nick']
        correo_modificar = request.session['usuario']['correo']
        perfil = Usuario.objects.get(user__username = user_modificar)

        if request.method == 'POST':
            usuario1 = request.POST.get('username','')
            codigo1 = request.POST.get('codigo','')
            nombre = request.POST.get('nombre','')
            apellido = request.POST.get('apellido','')
            correo = request.POST.get('correo', '')
            modificar = Usuario.objects.filter(user__username = user_modificar).update(codigo = codigo1)

            if not User.objects.exclude(username=user_modificar).filter(username=usuario1).exists():
                if not User.objects.exclude(email=correo_modificar).filter(email=correo).exists():
                    modificar_user = User.objects.filter(username = user_modificar).update(
                                                    username = usuario1, first_name = nombre,
                                                    last_name = apellido, email = correo)
                    usuario = Usuario.objects.get(user__username = usuario1)
                    usuario = {
                            'nick': usuario.user.username,
                            'correo': usuario.user.email,
                            'nombre': usuario.user.first_name,
                            'apellidos': usuario.user.last_name,
                            'codigo': usuario.codigo,
                            'rol': usuario.rol.id
                        }
                    #Se asigna una variable de sesión para poder acceder a ella desde cualquier página
                    request.session['usuario'] = usuario
                    request.session['just_logged'] = True
                    return panelInicio(request)
                else:
                    errors = "Ya esta siendo usado ese correo"
                    return render(request, 'Usuarios/modificar-perfil.html', locals())
            else:
                errors = "Ya existe usuario con ese nombre"
                return render(request, 'Usuarios/modificar-perfil.html', locals())
        else:
            return render(request, 'Usuarios/modificar-perfil.html', locals())        
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def modificar_password(request):
    if request.session['rol'] >= 1:
        form_size = 'small'

        if request.method == 'POST':
            password_actual = request.POST.get('password_actual','')
            password_nuevo = request.POST.get('password_nuevo','')
            verificacion_password = request.POST.get('verificacion_password','')
            #Autentificar que el usuario exista
            user_actual = request.session['usuario']['nick']
            usuario = User.objects.get(username=user_actual)
            #Si el usuario existe  y está activo, cambia contrase~a
            if password_nuevo == verificacion_password:
                usuario.set_password(password_nuevo)
                usuario.save()
                user = auth.authenticate(username=user_actual, password=password_nuevo)
                #Si el usuario existe  y está activo, se inicia la sesión
                auth.login(request, user)
                usuario = Usuario.objects.get(user=user)
                usuario = {
                        'nick': usuario.user.username,
                        'correo': usuario.user.email,
                        'nombre': usuario.user.first_name,
                        'apellidos': usuario.user.last_name,
                        'codigo': usuario.codigo,
                        'rol': usuario.rol.id
                    }
                #Se asigna una variable de sesión para poder acceder a ella desde cualquier página
                request.session['usuario'] = usuario
                request.session['rol'] = user.usuario.rol.id
                request.session['just_logged'] = True
                return panelInicio(request)
            else:
                errors = "Confirmacion de contraseña erronea"
                return render(request, TEMPLATE_MODIFICA_PASS, locals())
        else:
            return render(request, TEMPLATE_MODIFICA_PASS, locals())
    else:
        return redirect('error403', origen=request.path)

def login(request):
    if request.method == 'POST':
        #Tomar los valores mandados al hacer log in
        usuario = request.POST.get('username','')
        password = request.POST.get('pass','')
        
        #Autentificar que el usuario exista
        user = auth.authenticate(username=usuario, password=password)

        #Si el usuario existe  y está activo, se inicia la sesión
        if user is not None and user.is_active:
            auth.login(request, user)

            usuario = Usuario.objects.get(user=user)
            usuario = {
                    'nick': usuario.user.username,
                    'correo': usuario.user.email,
                    'nombre': usuario.user.first_name,
                    'apellidos': usuario.user.last_name,
                    'codigo': usuario.codigo,
                    'rol': usuario.rol.id
                }

            #Se asigna una variable de sesión para poder acceder a ella desde cualquier página
            request.session['usuario'] = usuario
            request.session['rol'] = user.usuario.rol.id
            request.session['just_logged'] = True

            return panelInicio(request)
        else:
            return render(request,'Usuarios/login.html', {'errors': "Usuario o contraseña incorrectos"})
    else:
        if request.user.is_authenticated():
            return panelInicio(request)
        else:
            return render(request, 'Usuarios/login.html')

def logout(request):
    try:
        auth.logout(request)
    except KeyError:
        pass
    return redirect('/')

def panelInicio(request):
    if request.user.is_authenticated():
        if request.session['rol'] == 1:
            return redirect('/inicio-alumno/')
        elif request.session['rol'] == 3:
            return redirect('/inicio-administrador/')
        else:
            return redirect('/inicio-administrador/')
    else:
        return redirect('/')

'''def nuevo_alumno(request):
    form_size = 'small'
    if request.method == 'POST':
        usuario = request.POST.get('username','')
        password = request.POST.get('password', '')
        codigo = request.POST.get('codigo','')
        nombre = request.POST.get('nombre','')
        apellido = request.POST.get('apellido','')
        correo = request.POST.get('correo', '')

        if User.objects.filter(Q(username=usuario) | Q(email=correo)).exists():
            errors = 'Ya existe registro con ese nombre'
            return render(request, 'Usuarios/nuevo-alumno.html', locals())
        else:
            nuevo_usuario = Usuario.alta_alumno(usuario, password, nombre, 
                                                apellido, correo, codigo)
            nuevo_usuario.save()
            #Autentificar que el usuario exista
            user = auth.authenticate(username=usuario, password=password)

            #Si el usuario existe  y está activo, se inicia la sesión
            if user is not None and user.is_active:
                auth.login(request, user)

                usuario = Usuario.objects.get(user=user)
                usuario = {
                        'nick': usuario.user.username,
                        'correo': usuario.user.email,
                        'nombre': usuario.user.first_name,
                        'apellidos': usuario.user.last_name,
                        'codigo': usuario.codigo,
                        'rol': usuario.rol.id
                    }

                #Se asigna una variable de sesión para poder acceder a ella desde cualquier página
                request.session['usuario'] = usuario
                request.session['rol'] = user.usuario.rol.id
                request.session['just_logged'] = True
                                
                return panelInicio(request)
    else:
        return render(request, 'Usuarios/nuevo-alumno.html', locals())'''
def nuevo_alumno(request):
    form_size = 'small'
    if request.method == 'POST':
        usuario = request.POST.get('username','')
        password = request.POST.get('password', '')
        codigo = request.POST.get('codigo','')
        nombre = request.POST.get('nombre','')
        apellido = request.POST.get('apellido','')
        correo = request.POST.get('correo', '')

        if User.objects.filter(Q(username=usuario) | Q(email=correo)).exists():
            errors = 'Ya existe registro con ese nombre'
            return render(request, 'Usuarios/nuevo-alumno.html', locals())
        else:
            nuevo_usuario = Usuario.alta_alumno(usuario, password, nombre, 
                                                apellido, correo, codigo)
            nuevo_usuario.save()
            #Autentificar que el usuario exista
            return redirect('/inicio-administrador/')
    else:
        return render(request, 'Usuarios/nuevo-alumno.html', locals())

def formato_pago(request):
    form_size = 'small'
    user_modificar = request.session['usuario']['nick']
    perfil = Usuario.objects.get(user__username = user_modificar)
    deuda = Pagos.objects.filter(user__username = user_modificar)
    print deuda
    return render(request, 'Cursos/format_pago.html', locals())

def seleccionar_cursos(request):
    cursos = Curso.objects.all()
    if request.method == 'POST':
        return redirect("/inicio-alumno/")
    else:
        return render(request,'Cursos/seleccionar_cursos.html', locals())

@login_required(login_url='/')
def activar_usuarios(request):
    if request.session['rol'] == 3:
        if request.method == 'POST':
            usuarios = Usuario.objects.filter(rol__id=1).order_by('user__username')

            for x in usuarios:
                estado = request.POST.get(x.user.username,'')

                if estado=='active' and not x.user.is_active:
                    x.user.is_active = True
                    x.user.save()
                elif estado=='unactive' and x.user.is_active:
                    x.user.is_active = False
                    x.user.save()

            return redirect('/inicio-administrador/',locals())
        else:
            usuarios = Usuario.objects.filter(rol__id=1).order_by('user__username')
            return render(request, 'Usuarios/activar-usuarios.html', locals())
    else:
        return redirect('error403', origen=request.path)

def activar_maestros(request):
    if request.session['rol'] == 3:
        if request.method == 'POST':
            usuarios = Usuario.objects.exclude(rol__id = 1 ).order_by('user__username')

            for x in usuarios:
                estado = request.POST.get(x.user.username,'')

                if estado=='active' and not x.user.is_active:
                    x.user.is_active = True
                    x.user.save()
                elif estado=='unactive' and x.user.is_active:
                    x.user.is_active = False
                    x.user.save()

            return redirect('/inicio-administrador/')
        else:
            usuarios = Usuario.objects.exclude(rol__id = 1).order_by('user__username')
            return render(request, 'Usuarios/activar-maestros.html', locals())
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def nueva_secretaria(request):
    if request.session['rol'] == 3:
        form_size = 'small'
        if request.method == 'POST':
            usuario = request.POST.get('username','')
            password = request.POST.get('password', '')
            codigo = request.POST.get('codigo','')
            nombre = request.POST.get('nombre','')
            apellido = request.POST.get('apellido','')
            correo = request.POST.get('correo', '')

            if User.objects.filter(Q(username=usuario) | Q(email=correo)).exists():
                errors = 'Ya existe registro con ese nombre'
                return render(request, 'Usuarios/nueva-secretaria.html', locals())
            else:
                nuevo_usuario = Usuario.alta_secretaria(usuario, password, nombre, 
                                                    apellido, correo, codigo)
                nuevo_usuario.save()
                #Autentificar que el usuario exista
                return redirect('/inicio-administrador/')
        else:
            return render(request, 'Usuarios/nueva-secretaria.html', locals())
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def nuevo_maestro(request):
    if request.session['rol'] == 3:
        form_size = 'small'
        if request.method == 'POST':
            usuario = request.POST.get('username','')
            password = request.POST.get('password', '')
            codigo = request.POST.get('codigo','')
            nombre = request.POST.get('nombre','')
            apellido = request.POST.get('apellido','')
            correo = request.POST.get('correo', '')

            if User.objects.filter(Q(username=usuario) | Q(email=correo)).exists():
                errors = 'Ya existe registro con ese nombre'
                return render(request, 'Usuarios/nuevo-maestro.html', locals())
            else:
                nuevo_usuario = Usuario.alta_maestro(usuario, password, nombre, 
                                                    apellido, correo, codigo)
                nuevo_usuario.save()
                #Autentificar que el usuario exista
                return redirect('/inicio-administrador/')
        else:
            return render(request, 'Usuarios/nuevo-maestro.html', locals())
    else:
        return redirect('error403', origen=request.path)

def lista_cursos(request):
    cursos = Curso.objects.all()
    if request.GET.get('materia'):
        materia = get_object_or_404(Curso, nombre=request.GET.get('materia'))
        if request.method == 'POST':
            try:
                selec = request.POST.get('materia','')
                curso = Curso.objects.get(nombre=selec)
                alumno = Usuario.objects.get(user__username=request.user.username)
                guardar = Listas(fk_alumno = alumno, fk_curso = curso)

                guardar.save()
                datos = " Curso a~adido "
                return render(request,'Cursos/lista_curso.html',locals())
            except:
                return render(request,'Cursos/seleccionar_cursos.html',locals())
        return render(request,'Cursos/seleccionar_cursos.html',locals())
    else:
        return render(request,'Cursos/lista_curso.html',locals())