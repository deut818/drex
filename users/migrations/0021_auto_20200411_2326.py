# Generated by Django 3.0.4 on 2020-04-11 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20200411_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.SlugField(blank=True, unique=True, verbose_name='username'),
        ),
    ]
