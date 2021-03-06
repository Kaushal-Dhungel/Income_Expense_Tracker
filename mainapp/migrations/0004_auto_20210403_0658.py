# Generated by Django 3.1.7 on 2021-04-03 06:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_expense_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=300, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='income',
            name='date',
            field=models.DateField(default=datetime.date(2020, 5, 6)),
            preserve_default=False,
        ),
    ]
