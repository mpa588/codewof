# Generated by Django 2.1.5 on 2019-07-16 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codewof', '0002_badge_earned_loginday_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='earned_badges',
            field=models.ManyToManyField(through='codewof.Earned', to='codewof.Badge'),
        ),
    ]