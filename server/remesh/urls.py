from django.urls import path

import remesh.views as views

app_name = 'remesh'
urlpatterns = [
    path('conversation', views.ConversationIndexView.as_view(), name='conversation_index'),
    path('conversation/add', views.ConversationAddView.as_view(), name='conversation_add')
]
