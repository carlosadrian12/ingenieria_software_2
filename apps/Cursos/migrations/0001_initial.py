# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nick', models.CharField(unique=True, max_length=20, validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z]*$', b'Use solo caracteres alfanumericos (a-Z, 0-9).')])),
                ('nombre', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inicio', models.CharField(max_length=40)),
                ('dias', models.CharField(max_length=30)),
                ('hora', models.CharField(max_length=20)),
                ('fk_Curso', models.ForeignKey(to='Cursos.Curso')),
            ],
        ),
    ]
