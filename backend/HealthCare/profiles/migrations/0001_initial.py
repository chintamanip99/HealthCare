# Generated by Django 3.2.4 on 2021-06-15 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctortype', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('age', models.IntegerField(default=65, null=True)),
                ('phone', models.CharField(max_length=12, null=True)),
                ('birthdate', models.CharField(max_length=100, null=True)),
                ('gender', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(max_length=500, null=True)),
                ('doctortype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.doctortype')),
            ],
        ),
    ]
