# Generated by Django 2.1.1 on 2018-11-07 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asesorias', '0010_cita_fechacita'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='suspendido',
            field=models.BooleanField(default=False),
        ),
    ]
