# Generated by Django 5.1.3 on 2024-12-27 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]