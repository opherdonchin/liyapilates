# Generated by Django 2.2.1 on 2019-06-10 22:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientlist', '0007_card_num_lessons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='card',
        ),
        migrations.AddField(
            model_name='card',
            name='begins_on',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='card',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clientlist.Client'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='held_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 10, 22, 0), unique=True),
        ),
    ]
