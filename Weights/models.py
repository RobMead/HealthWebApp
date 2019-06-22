from django.db import models
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User

class muscles(models.Model):
    """"List of muscles worked to relate to individual exercises. For example,
    both the chest press and peck deck machine would both work the chest."""

    muscle_worked = models.CharField(max_length=256)

    def __str__(self):
        return self.muscle_worked


class exercise_list(models.Model):
    """"List of exercises to be referenced from workout table."""

    exercise_name = models.CharField(max_length=256)
    muscle_worked = models.ForeignKey(muscles, on_delete=models.CASCADE)

    def __str__(self):
        return self.exercise_name


# class UserProfileInfo(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.user.username


class workout_diary(models.Model):
    """"Table to store individual exercises performed as part of a workout."""

    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    workout_date = models.DateField(default=date.today())
    exercise_name = models.ForeignKey(exercise_list, on_delete=models.CASCADE)
    reps = models.IntegerField()
    weight = models.IntegerField()
    notes = models.CharField(max_length=256, blank=True)

    def __str__(self):
        # return str(self.id) + ' ' + str(self.workout_date)
        return str(self.workout_date) + ' ' + str(self.exercise_name)

        def get_absolute_url(self):
            return reverse('sets')

            @classmethod
            def create(cls, **kwargs):
                workout = cls(kwargs)
                return workout
