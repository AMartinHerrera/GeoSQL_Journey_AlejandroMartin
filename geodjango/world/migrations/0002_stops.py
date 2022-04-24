# Generated by Django 3.2 on 2022-03-31 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop_name', models.CharField(blank=True, max_length=50)),
                ('commune_id', models.IntegerField(blank=True)),
                ('commune_name', models.CharField(blank=True, max_length=50)),
                ('x_coordinate', models.FloatField()),
                ('y_coordinate', models.FloatField()),
                ('mean_of_transport', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['stop_name'],
            },
        ),
    ]