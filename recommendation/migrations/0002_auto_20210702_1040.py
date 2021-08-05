# Generated by Django 3.2.3 on 2021-07-02 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='StatusCode',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='flag',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='productId',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='shortDescription',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='sku',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='zlQty',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]