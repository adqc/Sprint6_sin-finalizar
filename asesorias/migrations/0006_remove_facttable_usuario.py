# Generated by Django 2.1.1 on 2018-09-25 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asesorias', '0005_facttable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facttable',
            name='usuario',
        ),
    ]
