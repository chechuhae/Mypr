# Generated by Django 3.0.3 on 2020-03-27 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grp', '0022_auto_20200326_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='cicle',
            name='maximum',
            field=models.DateField(blank=True, null=True),
        ),
    ]
