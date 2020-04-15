# Generated by Django 2.1.5 on 2020-04-13 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_auto_20200412_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Electronics', 'Electronics'), ('Textbooks', 'Textbooks'), ('School supplies', 'School Supplies'), ('Pets', 'Pets'), ('Clothing', 'Clothing'), ('Housing', 'Housing'), ('Miscellaneous', 'Miscellaneous')], default='Miscellaneous', max_length=25),
        ),
    ]