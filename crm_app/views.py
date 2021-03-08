from django.shortcuts import render, get_object_or_404
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


class ProjectListView(generic.ListView):
    template_name = 'crm_app/project_list.html'
    def get_queryset(self):
        self.company = get_object_or_404(Company, pk=self.kwargs['pk'])
        return Project.objects.filter(company=self.company)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['pk'] = self.kwargs['pk']
        return context

class MessageCompanyListView(generic.ListView):
    template_name = 'crm_app/comp_message_list.html'
    def get_queryset(self):
        self.company = get_object_or_404(Company, pk=self.kwargs['pk'])
        return Message.objects.filter(project__company=self.company)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['pk'] = self.kwargs['pk']
        return context


class MessageProjectListView(generic.ListView):
    template_name = 'crm_app/proj_message_list.html'
    def get_queryset(self):
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return Message.objects.filter(project=self.project)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context




		
