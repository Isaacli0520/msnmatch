# Generated by Django 2.1.5 on 2019-07-25 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0024_course_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseuser',
            name='section',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
