# Generated by Django 3.0.4 on 2020-04-11 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20200411_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='slug',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.SlugField(default='username', unique=True, verbose_name='username'),
            preserve_default=False,
        ),
    ]
