from django.db import models
from django.core.validators import RegexValidator

#import time
from time import strftime

from apps.usuarios.models import Usuario

numerico = RegexValidator(r'^[0-9]*$', 'Use solo caracteres numericos (0-9).')
alfanumerico = RegexValidator(r'^[0-9a-zA-Z]*$', 'Use solo caracteres alfanumericos (a-Z, 0-9).')

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    nick = models.CharField(max_length=20, validators=[alfanumerico], unique=True)
    nombre = models.CharField(max_length=30)
    Seccion = models.CharField(max_length=120)
    maestro = models.OneToOneField(Usuario, blank=True, null=True)

    def __unicode__(self):
        return self.nombre
        pass

class Listas(models.Model):
    fk_curso = models.ForeignKey(Curso,blank=True, null=True)
    fk_alumno = models.ForeignKey(Usuario, blank=True, null=True)
    codigo = models.CharField(max_length=20 ,primary_key=True)
    
    def __unicode__(self):
        return str(self.codigo)
        pass
    