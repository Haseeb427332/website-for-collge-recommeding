# Generated by Django 2.2.5 on 2020-02-20 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200220_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data23',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]