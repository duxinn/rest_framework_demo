# Generated by Django 2.1.3 on 2019-02-26 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': '角色', 'verbose_name_plural': '角色'},
        ),
        migrations.AlterModelOptions(
            name='usertoken',
            options={'verbose_name': '用户token', 'verbose_name_plural': '用户token'},
        ),
        migrations.AlterModelTable(
            name='role',
            table='role',
        ),
        migrations.AlterModelTable(
            name='usertoken',
            table='user_token',
        ),
    ]
