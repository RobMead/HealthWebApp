# Generated by Django 2.2.1 on 2019-05-18 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Weights', '0007_auto_20190518_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout_diary',
            name='notes',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
