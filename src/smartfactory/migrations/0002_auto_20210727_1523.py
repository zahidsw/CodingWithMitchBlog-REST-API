# Generated by Django 3.2.3 on 2021-07-27 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartfactory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smartsearch',
            name='eti',
        ),
        migrations.RemoveField(
            model_name='smartsearch',
            name='groessen',
        ),
        migrations.RemoveField(
            model_name='smartsearch',
            name='vp',
        ),
        migrations.RemoveField(
            model_name='smartsearch',
            name='zlQty',
        ),
        migrations.AddField(
            model_name='smartsearch',
            name='productTags',
            field=models.JSONField(null=True),
        ),
    ]
