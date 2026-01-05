from django.urls import path
from . import views

urlpatterns = [
    # This connects the root of the 'core' app to your index view
    path('', views.index, name='index'),
]