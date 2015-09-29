# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cursos', '0004_auto_20150929_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listas',
            name='codigo',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
