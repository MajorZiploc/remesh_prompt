from django.urls import path

import remesh.views as views

app_name = 'remesh'
urlpatterns = [
    path('team', views.TeamIndexView.as_view(), name='team_index'),
    path('team/<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('team/add', views.TeamAddView.as_view(), name='team_add'),
    path('team/edit/<int:pk>', views.TeamEditView.as_view(), name='team_edit'),
    path('team/conversation/<int:team_pk>/', views.ConversationIndexView.as_view(), name='conversation_index'),
    path('conversation/<int:pk>/', views.ConversationDetailView.as_view(), name='conversation_detail'),
    path('conversation/add', views.ConversationAddView.as_view(), name='conversation_add'),
    path('conversation/edit/<int:pk>', views.ConversationEditView.as_view(), name='conversation_edit'),
]
