# Generated by Django 2.1.5 on 2019-05-04 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20190430_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='wechat',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
