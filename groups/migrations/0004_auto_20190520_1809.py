# Generated by Django 2.1.5 on 2019-05-20 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20190520_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_type',
            field=models.CharField(blank=True, choices=[('Family', 'Family'), ('Books', 'Books'), ('Film and TV', 'Film and TV'), ('General', 'General'), ('Game', 'Game'), ('Language', 'Language'), ('Academic Interests', 'Academic Interests'), ('Music', 'Music'), ('Sport', 'Sport'), ('Custom', 'Custom')], max_length=255),
        ),
    ]