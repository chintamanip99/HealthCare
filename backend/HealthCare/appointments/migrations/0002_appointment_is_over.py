# Generated by Django 3.2.4 on 2021-06-15 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_over',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
