# Generated by Django 2.1.2 on 2018-11-07 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_auto_20181107_0112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField()),
                ('clinicManager_location1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.ClinicLocation')),
            ],
        ),
    ]
