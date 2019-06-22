from django import forms
from Weights.models import workout_diary, muscles
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import UserProfileInfo

class WorkoutCreateForm(forms.ModelForm):

    class Meta:
        model = workout_diary
        fields = ['workout_date','exercise_name','reps','weight','notes']

    def __init__(self, user_id, *args, **kwargs):
        super(WorkoutCreateForm, self).__init__(*args, **kwargs)

        # set the user_id as an attribute of the form
        self.user_id = user_id

    def save(self, commit=True):
        instance = super(WorkoutCreateForm, self).save(commit=False)
        instance.user_id = self.user_id
        if commit:
            instance.save()
        return instance

class WorkoutCreateFormMulti(forms.ModelForm):
    reps2 = forms.IntegerField(required=False)
    reps3 = forms.IntegerField(required=False)
    reps4 = forms.IntegerField(required=False)
    reps5 = forms.IntegerField(required=False)

    class Meta:
        model = workout_diary
        fields = ['workout_date', 'exercise_name',
            'reps', 'reps2', 'reps3','reps4','reps5', 'weight', 'notes']

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1', 'password2')
