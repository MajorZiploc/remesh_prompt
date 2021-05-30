from django.urls import path

import remesh.views as views

app_name = 'remesh'
urlpatterns = [
    path('conversation', views.ConversationIndexView.as_view(), name='conversation_index'),
    path('conversation/<int:pk>/', views.ConversationDetailView.as_view(), name='conversation_detail'),
    path('conversation/add', views.ConversationAddView.as_view(), name='conversation_add'),
    path('conversation/edit/<int:pk>', views.ConversationEditView.as_view(), name='conversation_edit'),
]
