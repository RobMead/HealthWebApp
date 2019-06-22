import datetime
from . import forms
from . import models
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, FormView, DeleteView
)
from django.shortcuts import (
    render, redirect, render_to_response, HttpResponseRedirect
    )
from django.db.models import Sum, Count
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

class sets_view(TemplateView):
    template_name = 'sets_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = models.workout_diary

        today  = datetime.date.today()
        diff = 6 - today.timetuple()[6]
        diff = datetime.timedelta(days=diff)
        today = today + diff
        week_ago = today - datetime.timedelta(days=7)
        two_week_ago = week_ago - datetime.timedelta(days=7)

        aggregate = {}

        user = self.request.user
        # If user hasn't logged in then show default dataset instead ie. for
        # user with id 1.
        if not self.request.user.is_authenticated:
            user = 1

        queryset = model.objects.filter(user=user).filter(
            workout_date__range=(week_ago + datetime.timedelta(days=1), today)
            ).values(
                'exercise_name_id__muscle_worked_id__muscle_worked'
                ).annotate(Count('reps'))
        for entry in queryset:
            muscle = entry['exercise_name_id__muscle_worked_id__muscle_worked']
            aggregate[muscle] = [entry['reps__count'],0]

        queryset = model.objects.filter(user=user).filter(
            workout_date__range=(two_week_ago + datetime.timedelta(days=1), week_ago)
            ).values(
                'exercise_name_id__muscle_worked_id__muscle_worked'
                ).annotate(Count('reps'))
        for entry in queryset:
            muscle = entry['exercise_name_id__muscle_worked_id__muscle_worked']
            if muscle in aggregate:
                aggregate[muscle][1] = entry['reps__count']
            else:
                aggregate[muscle] = [0,entry['reps__count']]

        context['weekly_sets'] = aggregate
        print(context)
        return context

class workout_list_m_view(ListView):

    template_name = 'workout_list_m.html'
    model = models.workout_diary
    context_object_name = 'workout_list'

    def get_queryset(self):
        user = self.request.user
        model = models.workout_diary

        # If user hasn't logged in then show default dataset instead ie. for
        # user with id 1.
        if not self.request.user.is_authenticated:
            user = 1

        queryset = model.objects.filter(user=user).values(
            'id',
            'workout_date',
            'exercise_name_id__exercise_name',
            'weight',
            'reps',
            'exercise_name_id__muscle_worked_id',
            'exercise_name_id__muscle_worked_id__muscle_worked'
            ).order_by(
                    'exercise_name_id__muscle_worked_id__muscle_worked',
                    '-workout_date',
                    'exercise_name_id__exercise_name',
                )
        return queryset

class workout_list_d_view(ListView):

    template_name = 'workout_list_d.html'
    model = models.workout_diary
    context_object_name = 'workout_list'

    def get_queryset(self):
        user = self.request.user
        model = models.workout_diary

        # If user hasn't logged in then show default dataset instead ie. for
        # user with id 1.
        if not self.request.user.is_authenticated:
            user = 1

        queryset = model.objects.filter(user=user).values(
            'id',
            'workout_date',
            'exercise_name_id__exercise_name',
            'weight',
            'reps',
            'exercise_name_id__muscle_worked_id',
            'exercise_name_id__muscle_worked_id__muscle_worked'
            ).order_by(
                    '-workout_date',
                    'exercise_name_id__muscle_worked_id__muscle_worked',
                    'exercise_name_id__exercise_name',
                )

        return queryset

class workout_list_e_view(ListView):
    template_name = 'workout_list_e.html'
    model = models.workout_diary
    context_object_name = 'workout_list'

    def get_queryset(self):
        user = self.request.user
        model = models.workout_diary

        # If user hasn't logged in then show default dataset instead ie. for
        # user with id 1.
        if not self.request.user.is_authenticated:
            user = 1

        queryset = model.objects.filter(user=user).values(
        'id',
        'workout_date',
        'exercise_name_id__exercise_name',
        'weight',
        'reps',
        'exercise_name_id__muscle_worked_id',
        'exercise_name_id__muscle_worked_id__muscle_worked'
        ).order_by(
        'exercise_name_id__exercise_name',
        '-workout_date',
        'exercise_name_id__muscle_worked_id__muscle_worked',
        )

        return queryset

class WorkoutCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_class = forms.WorkoutCreateForm
    template_name = 'workout_create.html'
    success_url = reverse_lazy('wo_create')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(WorkoutCreateView, self).get_form_kwargs(*args,**kwargs)
        kwargs['user_id'] = self.request.user.pk
        return kwargs

@login_required(login_url = '/login/')
def WorkoutCreateViewMulti(request):

    woforms = [None] * 5
    # Name of each reps field from the form
    reps_list = ["reps", "reps2", "reps3", "reps4", "reps5"]
    combined = zip(woforms, reps_list)

    if request.method == "POST":
        for form, repsfield in combined:
            form = forms.WorkoutCreateFormMulti(
                request.POST, instance=models.workout_diary())

            if form.is_valid() and form.cleaned_data[repsfield] != None:
                new_wo = form.save(commit=False)
                new_wo.user_id = request.user.id
                new_wo.reps = form.cleaned_data[repsfield]
                new_wo.save()

        return HttpResponseRedirect(reverse_lazy('wo_create_multi'))
    else:
        wo = forms.WorkoutCreateFormMulti(instance=models.workout_diary())

    return render(request,'workout_create_multi.html', {'form': wo})

class WorkoutDeleteView(DeleteView):
    model = models.workout_diary
    template_name = 'workout_diary_confirm_delete.html'
    success_url = reverse_lazy("workouts_m")

def signup(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = forms.UserForm()
    return render(request, 'registration/signup.html', {'form': form})

class Login_view(LoginView):
    # Set the url redirect for succesful login.
    extra_context = {'next':'index'}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context.keys())
        return context

class Logout_view(LogoutView):
    template_name: 'index.html'
    next_page = reverse_lazy("index")
