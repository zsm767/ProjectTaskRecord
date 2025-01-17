# Generated by Django 2.2 on 2019-06-04 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobimport', '0013_auto_20190530_0849'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobs',
            options={'ordering': ['job_id']},
        ),
        migrations.AddField(
            model_name='taskcodes',
            name='accumulated_budget',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=19),
        ),
        migrations.AddField(
            model_name='taskcodes',
            name='accumulated_footage',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
