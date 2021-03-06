# Generated by Django 2.1.2 on 2018-11-19 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0024_auto_20181116_0958'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('firstname', models.CharField(blank=True, max_length=200, null=True)),
                ('lastname', models.CharField(blank=True, max_length=200, null=True)),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('password', models.CharField(blank=True, max_length=200, null=True)),
                ('role', models.CharField(max_length=200)),
                ('emailID', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('token', models.CharField(blank=True, max_length=200, null=True)),
                ('clinic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db.ClinicLocation')),
            ],
        ),
        migrations.RemoveField(
            model_name='clinicmanager',
            name='clinicLocation',
        ),
        migrations.DeleteModel(
            name='ClinicManager',
        ),
    ]
