# Generated by Django 2.1.5 on 2019-07-23 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0021_remove_course_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('school', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Department',
        ),
    ]
