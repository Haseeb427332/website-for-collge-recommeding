# Generated by Django 2.2.5 on 2020-05-03 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20200503_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_data23',
            name='is_active',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='user_data23',
            name='last_login',
            field=models.DateField(auto_now_add=True),
        ),
    ]