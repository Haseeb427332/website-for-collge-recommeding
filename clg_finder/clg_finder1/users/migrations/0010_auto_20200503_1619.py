# Generated by Django 2.2.5 on 2020-05-03 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200503_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_data23',
            name='last_login',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]