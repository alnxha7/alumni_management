# Generated by Django 4.2.3 on 2024-11-13 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumini', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
