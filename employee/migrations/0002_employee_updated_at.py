# Generated by Django 5.1.4 on 2025-01-25 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
    ]
