# Generated by Django 3.1.3 on 2021-01-04 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_planprofileversion_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='planprofileversion',
            name='user_agent',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
