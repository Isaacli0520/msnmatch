# Generated by Django 2.1.5 on 2020-04-15 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_planprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='year',
        ),
        migrations.AlterField(
            model_name='profile',
            name='graduate_year',
            field=models.CharField(blank=True, choices=[('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], max_length=255),
        ),
    ]