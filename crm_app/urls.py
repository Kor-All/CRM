from django.urls import path
from . import views


urlpatterns = [
	path('', views.CompanyListView.as_view(), name='index'),
	path('company/<int:pk>/projects/', views.ProjectListView.as_view(), name='projects'),
	path('company/<int:pk>/messages/', views.MessageCompanyListView.as_view(), name='comp_messages'),
	path('company/<int:pk>', views.CompanyDetailView.as_view(), name='company_detail'),
	path('company/create/', views.CompanyCreate.as_view(), name='company_create'),
    path('company/<int:pk>/update/', views.CompanyUpdate.as_view(), name='company_update'),
	path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
	path('project/<int:pk>/messages/', views.MessageProjectListView.as_view(), name='proj_messages'),
	path('project/create/', views.ProjectCreate.as_view(), name='project_create'),
    path('project/<int:pk>/update/', views.ProjectUpdate.as_view(), name='project_update'),
	path('message/<int:pk>', views.MessageDetailView.as_view(), name='message_detail'),
	path('message/create/', views.MessageCreate.as_view(), name='message_create'),
    path('message/<int:pk>/update/', views.MessageUpdate.as_view(), name='message_update'),
	path('messages/', views.UsersMessageListView.as_view(), name='users_messages'),
]
																										