# Generated by Django 5.0.6 on 2024-06-08 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BOOKS', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='ISBN',
        ),
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]