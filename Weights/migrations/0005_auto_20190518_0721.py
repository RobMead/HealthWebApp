# Generated by Django 2.2.1 on 2019-05-18 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Weights', '0004_exercise_list_muscle_worked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise_list',
            name='muscle_worked',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Weights.muscles'),
        ),
        migrations.AlterField(
            model_name='workout_diary',
            name='workout_date',
            field=models.DateField(auto_now=True),
        ),
    ]
