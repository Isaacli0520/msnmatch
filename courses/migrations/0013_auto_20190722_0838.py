# Generated by Django 2.1.5 on 2019-07-22 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_course_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseuser',
            old_name='rating',
            new_name='rating_course',
        ),
        migrations.AddField(
            model_name='courseuser',
            name='rating_professor',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
