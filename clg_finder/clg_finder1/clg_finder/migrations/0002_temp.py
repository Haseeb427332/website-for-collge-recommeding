# Generated by Django 2.2.5 on 2020-05-09 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clg_finder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='temp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Orign_clg_id', models.IntegerField()),
                ('clg_id', models.IntegerField()),
                ('clg_name', models.CharField(max_length=1000)),
                ('District', models.CharField(max_length=20)),
                ('University', models.CharField(max_length=100)),
                ('contact_details', models.TextField()),
            ],
        ),
    ]
