# Generated by Django 3.2.3 on 2021-07-06 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0002_auto_20210702_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='groessen',
            field=models.JSONField(default='null'),
            preserve_default=False,
        ),
    ]
