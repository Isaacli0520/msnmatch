# Generated by Django 2.1.5 on 2019-07-07 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20190707_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='number',
            field=models.IntegerField(default='0'),
        ),
    ]