# Generated by Django 2.1.5 on 2019-07-07 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseInstructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(default='Null', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CourseUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('take', models.CharField(default='Null', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Null', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='Null')),
            ],
        ),
        migrations.RemoveField(
            model_name='relation',
            name='course',
        ),
        migrations.RemoveField(
            model_name='relation',
            name='user',
        ),
        migrations.RemoveField(
            model_name='course',
            name='course_name',
        ),
        migrations.RemoveField(
            model_name='course',
            name='course_number',
        ),
        migrations.RemoveField(
            model_name='course',
            name='course_users',
        ),
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='mnemonic',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='course',
            name='number',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='course',
            name='title',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='topic',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='units',
            field=models.IntegerField(default='0'),
        ),
        migrations.DeleteModel(
            name='Relation',
        ),
        migrations.AddField(
            model_name='review',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
        migrations.AddField(
            model_name='review',
            name='course_instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.CourseInstructor'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courseuser',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
        migrations.AddField(
            model_name='courseuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courseinstructor',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
        migrations.AddField(
            model_name='courseinstructor',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(through='courses.CourseInstructor', to='courses.Instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='users',
            field=models.ManyToManyField(through='courses.CourseUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
