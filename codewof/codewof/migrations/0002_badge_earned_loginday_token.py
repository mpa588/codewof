# Generated by Django 2.1.5 on 2019-07-02 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codewof', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_name', models.CharField(max_length=100, unique=True)),
                ('display_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('icon_name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Earned',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codewof.Badge')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codewof.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='LoginDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codewof.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=500)),
            ],
        ),
    ]