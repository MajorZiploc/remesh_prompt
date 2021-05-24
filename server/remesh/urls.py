from django.urls import path

from . import views

app_name = 'remesh'
urlpatterns = [
    path('team', views.TeamIndexView.as_view(), name='team_index'),
    path('team/<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('day', views.DayIndexView.as_view(), name='day_index'),
    path('day/<int:pk>/', views.DayDetailView.as_view(), name='day_detail'),
    path('day/add', views.AddDayView.as_view(), name='add_day')
]
