# Generated by Django 2.1.2 on 2018-12-01 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0036_auto_20181201_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
