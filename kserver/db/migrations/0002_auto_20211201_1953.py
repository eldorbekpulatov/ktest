# Generated by Django 3.2.6 on 2021-12-01 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ('serial', 'user', 'station', 'product', 'model')},
        ),
        migrations.AlterModelOptions(
            name='instrument',
            options={'ordering': ('name', 'type', 'serialNumber', 'kepcoNumber', 'calibrationDate', 'expirationDate')},
        ),
        migrations.AlterModelOptions(
            name='log',
            options={'ordering': ('card', 'script', 'file', 'status')},
        ),
        migrations.RemoveField(
            model_name='station',
            name='instruments',
        ),
        migrations.AddField(
            model_name='instrument',
            name='station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ad.station'),
        ),
        migrations.AlterField(
            model_name='log',
            name='status',
            field=models.CharField(blank=True, choices=[('FAILED', 'FAILED'), ('PASSED', 'PASSED')], max_length=10, null=True),
        ),
    ]
