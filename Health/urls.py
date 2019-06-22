"""Health URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Weights import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('wo_d/',views.workout_list_d_view.as_view(), name = 'workouts'),
    path('wo_e/',views.workout_list_e_view.as_view(), name = 'workouts_e'),
    path('wo_m/',views.workout_list_m_view.as_view(), name = 'workouts_m'),
    path('sets/',views.sets_view.as_view(), name = 'sets'),
    path('wo_create/',views.WorkoutCreateView.as_view(), name = 'wo_create'),
    path('wo_create_multi/',views.WorkoutCreateViewMulti, name = 'wo_create_multi'),
    path('delete/<pk>/',views.WorkoutDeleteView.as_view(), name='delete'),
    path('register/', views.signup, name='register'),
    path('login/', views.Login_view.as_view(), name='login'),
    path('logout/', views.Logout_view.as_view(), name='logout'),

]
