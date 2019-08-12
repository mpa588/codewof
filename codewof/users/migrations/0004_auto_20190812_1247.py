# Generated by Django 2.1.5 on 2019-08-12 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190812_0150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usertype',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='usertype',
            name='order',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='users.UserType', verbose_name='Are you a student or teacher?'),
        ),
    ]
