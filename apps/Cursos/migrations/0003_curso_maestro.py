# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('Cursos', '0002_auto_20150821_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='maestro',
            field=models.OneToOneField(null=True, blank=True, to='usuarios.Usuario'),
        ),
    ]
