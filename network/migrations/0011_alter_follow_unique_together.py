# Generated by Django 4.2.5 on 2023-12-26 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_alter_likes_post'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('user', 'followed')},
        ),
    ]