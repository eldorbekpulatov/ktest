# Generated by Django 3.2.6 on 2021-12-02 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0004_auto_20211202_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='status',
            field=models.CharField(blank=True, choices=[('0', 'FAILED'), ('1', 'PASSED')], max_length=10, null=True),
        ),
    ]
