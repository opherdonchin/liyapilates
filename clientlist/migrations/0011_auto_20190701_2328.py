# Generated by Django 2.2.2 on 2019-07-01 23:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientlist', '0010_auto_20190623_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='held_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 1, 23, 0), unique=True),
        ),
    ]
