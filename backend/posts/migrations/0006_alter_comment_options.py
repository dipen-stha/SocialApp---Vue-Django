# Generated by Django 5.1.3 on 2024-12-04 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_comment_like'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
    ]
