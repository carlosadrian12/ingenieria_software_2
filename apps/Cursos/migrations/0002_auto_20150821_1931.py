# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Cursos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='horario',
            old_name='fk_Curso',
            new_name='curso',
        ),
        migrations.AddField(
            model_name='curso',
            name='Seccion',
            field=models.CharField(default=datetime.datetime(2015, 8, 22, 0, 31, 17, 345723, tzinfo=utc), max_length=120),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='curso',
            name='nombre',
            field=models.CharField(max_length=30),
        ),
    ]
