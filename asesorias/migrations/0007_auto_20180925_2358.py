# Generated by Django 2.1.1 on 2018-09-25 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asesorias', '0006_remove_facttable_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='comentario',
            field=models.CharField(default='null', max_length=255),
        ),
        migrations.AddField(
            model_name='cita',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
