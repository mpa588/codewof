# Generated by Django 2.1.5 on 2019-07-31 22:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('codewof', '0006_auto_20190801_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='earned',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]