# Generated by Django 2.1.5 on 2020-04-12 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='conditions',
            new_name='condition',
        ),
    ]
