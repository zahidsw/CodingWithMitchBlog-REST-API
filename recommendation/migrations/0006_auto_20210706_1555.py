# Generated by Django 3.2.3 on 2021-07-06 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0005_auto_20210706_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='categories',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='groessen',
            field=models.TextField(blank=True, null=True),
        ),
    ]
