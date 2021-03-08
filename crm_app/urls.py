from django.urls import path
from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('company/<int:pk>/projects/', views.ProjectListView.as_view(), name='projects'),
	path('company/<int:pk>/messages/', views.MessageCompanyListView.as_view(), name='comp_messages'),
	path('company/<int:pk>', views.CompanyDetailView.as_view(), name='company_detail'),
	path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
	path('project/<int:pk>/messages/', views.MessageProjectListView.as_view(), name='proj_messages'),
	path('message/<int:pk>', views.MessageDetailView.as_view(), name='message_detail'),
]
