# Generated by Django 2.1.5 on 2019-07-14 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20190707_0639'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='prerequisite',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
