# Generated by Django 2.2 on 2019-04-24 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobimport', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='job_id',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='taskcodes',
            name='phase',
            field=models.CharField(default='00', max_length=2),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(max_length=8),
        ),
    ]
