# Generated by Django 2.2.5 on 2020-02-22 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200222_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data23',
            name='profile_pic',
            field=models.ImageField(default=1, upload_to='pictures'),
            preserve_default=False,
        ),
    ]
