# Generated by Django 3.2.6 on 2021-12-02 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0006_alter_log_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='status',
            field=models.CharField(blank=True, choices=[('FAIL', 'FAILED'), ('PASS', 'PASSED')], max_length=10, null=True),
        ),
    ]
