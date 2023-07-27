# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('age_submission/', views.age_submission_view, name='age_submission_view'),
    # Other URL patterns if you have more views
]
