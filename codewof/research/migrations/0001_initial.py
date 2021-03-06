# Generated by Django 2.1.5 on 2019-08-13 03:48

import autoslug.fields
import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, null=True, populate_from='title')),
                ('title', models.CharField(max_length=200)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('visible', models.BooleanField(default=False, help_text='Set to true when study should be listed to users.')),
                ('consent_form', models.CharField(blank=True, help_text='Name of class for consent form.', max_length=200)),
            ],
            options={
                'verbose_name': 'study',
                'verbose_name_plural': 'studies',
                'ordering': ['start_date', 'end_date'],
            },
        ),
        migrations.CreateModel(
            name='StudyGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Name of group, hidden from users and source control.', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='StudyRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('send_study_results', models.BooleanField(default=False)),
                ('study_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='research.StudyGroup')),
            ],
        ),
    ]
