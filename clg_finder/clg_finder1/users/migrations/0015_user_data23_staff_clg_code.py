# Generated by Django 2.2.5 on 2020-05-04 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20200504_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data23',
            name='staff_clg_code',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
