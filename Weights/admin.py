from django.contrib import admin
from Weights.models import exercise_list, workout_diary, muscles #UserProfileInfo

# Register your models here.
admin.site.register(exercise_list)
admin.site.register(workout_diary)
admin.site.register(muscles)
# admin.site.register(UserProfileInfo)
