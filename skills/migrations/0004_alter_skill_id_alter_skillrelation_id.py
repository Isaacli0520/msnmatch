# Generated by Django 4.0.3 on 2022-05-14 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0003_auto_20200418_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='skillrelation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
