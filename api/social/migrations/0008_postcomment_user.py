# Generated by Django 5.0.7 on 2024-07-21 00:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('social', '0007_rename_post_comments_post_comment_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile'),
            preserve_default=False,
        ),
    ]
