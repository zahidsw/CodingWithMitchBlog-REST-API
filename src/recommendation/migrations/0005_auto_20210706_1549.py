# Generated by Django 3.2.3 on 2021-07-06 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0004_alter_recommendation_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='categories',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='groessen',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
