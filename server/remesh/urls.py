from django.urls import path

import remesh.views as views

app_name = 'remesh'
urlpatterns = [
    path('team', views.TeamIndexView.as_view(), name='team_index'),
    path('team/<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('team/add', views.TeamAddView.as_view(), name='team_add'),
    path('team/edit/<int:pk>', views.TeamEditView.as_view(), name='team_edit'),
    path('team/delete/<int:pk>', views.TeamDeleteView.as_view(), name='team_delete'),
    path('team/conversation/<int:team_pk>/', views.ConversationIndexView.as_view(), name='team_conversation_index'),
    path('team/past-conversation/<int:team_pk>/', views.ConversationPastView.as_view(), name='team_conversation_past'),
    path('team/future-conversation/<int:team_pk>/', views.ConversationFutureView.as_view(), name='team_conversation_future'),
    path('team/active-conversation/<int:team_pk>/', views.ConversationActiveView.as_view(), name='team_conversation_active'),
    path('conversation/<int:pk>/', views.ConversationDetailView.as_view(), name='conversation_detail'),
    path('conversation/add', views.ConversationAddView.as_view(), name='conversation_add'),
    path('conversation/edit/<int:pk>', views.ConversationEditView.as_view(), name='conversation_edit'),
]
