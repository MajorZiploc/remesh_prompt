from django.urls import path

from . import views

app_name = 'body_comp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('add_day', views.AddDayView.as_view(), name='add_day')
]
