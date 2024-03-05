"""
URL mappings for the user API
"""
from django.urls import path

from user import views


app_name = 'user'
#defines pattern for url - anything passed will be handled by this view

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]