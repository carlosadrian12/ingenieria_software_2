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

    def __unicode__(self):
        return self.nombre
        pass

class Horario(models.Model):
	inicio = models.CharField(max_length=40)
	dias = models.CharField(max_length=30)
	hora = models.CharField(max_length=20)
	curso = models.ForeignKey(Curso)

	def  __unicode__(self):
		return self.inicio
		pass
