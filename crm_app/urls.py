from django.urls import path
from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('company/<int:pk>', views.CompanyDetailView.as_view(), name='company_detail'),
	# path('project/<int:pk>/messages/', views.MessageListView.as_view(), name='messages'),
	path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
	path('message/<int:pk>', views.MessageDetailView.as_view(), name='message_detail'),
]
