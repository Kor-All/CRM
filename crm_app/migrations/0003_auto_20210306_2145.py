# Generated by Django 3.1.7 on 2021-03-06 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0002_auto_20210306_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='rating',
            field=models.CharField(choices=[('vg', 'Отлично'), ('g', 'Хорошо'), ('n', 'Нейтрально'), ('b', 'Плохо'), ('vb', 'Очень плохо')], max_length=2),
        ),
    ]
