# Generated by Django 2.2 on 2020-04-17 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_coursetag'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否广告位'),
        ),
    ]
