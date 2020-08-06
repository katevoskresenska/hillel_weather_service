# Generated by Django 3.0.7 on 2020-08-05 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='id',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='cloud_counter',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='datetime',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='precipitation',
        ),
        migrations.AddField(
            model_name='country',
            name='flag',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='wiki_page',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='weather',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.Country'),
        ),
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='weather',
            name='humidity',
            field=models.CharField(max_length=20),
        ),
        migrations.RemoveField(
            model_name='weather',
            name='location',
        ),
        migrations.AddField(
            model_name='weather',
            name='location',
            field=models.ManyToManyField(to='weather.Location'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='pressure',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='weather',
            name='temp_feels_like',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='weather',
            name='temp_max',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='weather',
            name='temp_min',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='weather',
            name='temperature',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='weather',
            name='visibility',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='weather',
            name='wind_deg',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='weather',
            name='wind_speed',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together={('longitude', 'latitude')},
        ),
    ]