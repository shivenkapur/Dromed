# Generated by Django 2.1.2 on 2018-11-16 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0023_order_assigned'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoredValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latestOrderNo', models.IntegerField()),
                ('latestDeliveryNo', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='profile_image',
            field=models.ImageField(upload_to=''),
        ),
    ]
