from django.urls import path

from . import views

app_name = 'remesh'
urlpatterns = [
    path('', views.DayIndexView.as_view(), name='index'),
    path('<int:pk>/', views.DayDetailView.as_view(), name='detail'),
    path('add_day', views.AddDayView.as_view(), name='add_day')
]
