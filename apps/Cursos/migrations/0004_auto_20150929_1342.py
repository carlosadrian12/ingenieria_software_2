# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('Cursos', '0003_curso_maestro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listas',
            fields=[
                ('codigo', models.IntegerField(default=10, serialize=False, primary_key=True)),
                ('fk_alumno', models.ForeignKey(blank=True, to='usuarios.Usuario', null=True)),
                ('fk_curso', models.ForeignKey(blank=True, to='Cursos.Curso', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='horario',
            name='curso',
        ),
        migrations.DeleteModel(
            name='Horario',
        ),
    ]
