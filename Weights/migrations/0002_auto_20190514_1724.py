# Generated by Django 2.2.1 on 2019-05-14 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Weights', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout_diary',
            name='workout_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]