# Generated by Django 4.2.5 on 2024-01-05 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_remove_posts_liked_user_likes'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='likes',
            unique_together={('user', 'post')},
        ),
    ]
