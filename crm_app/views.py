from django.shortcuts import render
from django.views import generic
from .models import Company, Address, Phone, Email, Project, Message

# Create your views here.

def index(request):
	all_comp = Company.objects.all()
	# phone = all_comp.phone

	return render(request, 'index.html', 
		context={'all_comp': all_comp},
    )


class CompanyDetailView(generic.DetailView):
    model = Company


class ProjectDetailView(generic.DetailView):
    model = Project


class MessageDetailView(generic.DetailView):
    model = Message

	
		
