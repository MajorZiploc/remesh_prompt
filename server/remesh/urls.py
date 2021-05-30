from django.urls import path

import remesh.views as views

app_name = 'remesh'
urlpatterns = [
    path('conversation', views.ConversationIndexView.as_view(), name='conversation_index'),
    path('conversation/add', views.ConversationAddView.as_view(), name='conversation_add'),
    path('message/<int:conversation_pk>', views.MessageIndexView.as_view(), name='message_index'),
    path('message/add/<int:conversation_pk>', views.MessageAddView.as_view(), name='message_add'),
]
