# Generated by Django 3.2.3 on 2021-07-06 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0006_auto_20210706_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='categories',
            field=models.JSONField(default='null'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='groessen',
            field=models.JSONField(default='null'),
            preserve_default=False,
        ),
    ]