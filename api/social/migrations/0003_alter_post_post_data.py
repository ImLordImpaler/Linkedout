# Generated by Django 5.0.7 on 2024-07-20 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_post_post_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_data',
            field=models.JSONField(default=dict),
        ),
    ]
