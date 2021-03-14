from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.forms import formset_factory
from .models import Company, Address, Phone, Email, Project, Message
from .forms import CompanyForm, AddressFormSet, PhoneFormSet, EmailFormSet


# Create your views here.


class CompanyListView(LoginRequiredMixin, generic.ListView):
    """A class used to represent all companies

    Attributes:
        model (class): Database's table
        paginate_by (int): Number of records on the page
        template_name (str): Name of html template for rendering
    """
    model = Company
    paginate_by = 3
    template_name = 'index.html'


    def get_ordering(self):
        """Method sort records on the page

        Attributes:
            ordering (QuerySet): Sorted list of companies
        """
        ordering = self.request.GET.get('orderby')
        return ordering


class CompanyDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    """A class used to represent information of company

    Attributes:
        model (var): Database's table
        permission_required (str): Page access for manager and administrators
    """
    model = Company
    permission_required = 'crm_app.view_company'


class ProjectDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    """A class used to represent information of project

    Attributes:
        model (class): Database's table
        permission_required (str): Page access for manager and administrators
    """
    model = Project
    permission_required = 'crm_app.view_project'


class MessageDetailView(PermissionRequiredMixin, generic.DetailView):
    """A class used to represent information of message

    Attributes:
        model (class): Database's table
        permission_required (str): Page access for manager and administrators
    """
    model = Message
    permission_required = 'crm_app.view_message'



class ProjectListView(PermissionRequiredMixin, generic.ListView):
    """A class used to represent all projects of company

    Attributes:
        template_name (str): Name of html template for rendering
        permission_required (str): Page access for manager and administrators
    """
    template_name = 'crm_app/project_list.html'
    permission_required = 'crm_app.view_project'
    def get_queryset(self):
        """Overriding QuerySet

        Returns:
            QuerySet of projects.
            Can be sorted.
        """
        self.company = get_object_or_404(Company, pk=self.kwargs['pk'])
        return Project.objects.filter(company=self.company).order_by(self.request.GET.get('orderby', 'name'))

    def get_context_data(self, **kwargs):
        """Get the context for this view.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['pk'] = self.kwargs['pk']
        return context


class MessageCompanyListView(PermissionRequiredMixin, generic.ListView):
    """A class used to represent all messages of company

    Attributes:
        template_name (str): Name of html template for rendering
        permission_required (str): Page access for manager and administrators
    """
    template_name = 'crm_app/comp_message_list.html'
    permission_required = 'crm_app.view_message'

    def get_queryset(self):
        """Overriding QuerySet

        Returns:
            QuerySet of messages.
            Can be sorted and filtered.
        """
        self.company = get_object_or_404(Company, pk=self.kwargs['pk'])
        return Message.objects.filter(project__company=self.company).\
        order_by(self.request.GET.get('orderby', 'date_time')).\
        filter(description__contains=self.request.GET.get('filter', ''))

    def get_context_data(self, **kwargs):
        """Get the context for this view.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['pk'] = self.kwargs['pk']
        return context


class MessageProjectListView(PermissionRequiredMixin, generic.ListView):
    """A class used to represent all messages of project

    Attributes:
        template_name (str): Name of html template for rendering
        permission_required (str): Page access for manager and administrators
    """
    template_name = 'crm_app/proj_message_list.html'
    permission_required = 'crm_app.view_message'

    def get_queryset(self):
        """Overriding QuerySet

        Returns:
            QuerySet of messages.
            Can be sorted and filtered.
        """
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return Message.objects.filter(project=self.project).\
        order_by(self.request.GET.get('orderby', 'date_time')).\
        filter(description__contains=self.request.GET.get('filter', ''))

    def get_context_data(self, **kwargs):
        """Get the context for this view.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        context['pk'] = self.kwargs['pk']
        return context


class CompanyCreate(PermissionRequiredMixin, CreateView):
    """A class used to create a company

    Attributes:
        model (class): Database's table
        form_class (class): Class inherit from ModelForm
        permission_required (str): Page access for manager and administrators
    """
    model = Company
    form_class = CompanyForm
    permission_required = 'crm_app.add_company'


    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        address_form = AddressFormSet()
        phone_form = PhoneFormSet()
        email_form = EmailFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  address_form=address_form,
                                  phone_form=phone_form,
                                  email_form=email_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        address_form = AddressFormSet(self.request.POST)
        phone_form = PhoneFormSet(self.request.POST)
        email_form = EmailFormSet(self.request.POST)
        if (form.is_valid() and address_form.is_valid() and
            phone_form.is_valid() and email_form.is_valid()):
            return self.form_valid(form, address_form, phone_form, email_form)
        else:
            return self.form_invalid(form, address_form, phone_form, email_form)

    def form_valid(self, form, address_form, phone_form, email_form):
        """
        Called if all forms are valid. Creates a Company instance along with
        associated Address and Phones and Emails and then redirects to a
        success page.
        """
        self.object = form.save()
        address_form.instance = self.object
        address_form.save()
        phone_form.instance = self.object
        phone_form.save()
        email_form.instance = self.object
        email_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, address_form, phone_form, email_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  address_form=address_form,
                                  phone_form=phone_form,
                                  email_form=email_form))



class CompanyUpdate(PermissionRequiredMixin, UpdateView):
    """A class used to update a company

    Attributes:
        model (class): Database's table
        form_class (class): Class inherit from ModelForm
        permission_required (str): Page access for manager and administrators
    """
    model = Company
    form_class = CompanyForm
    permission_required = 'crm_app.change_company'


    def get_context_data(self, **kwargs):
        """Overriding QuerySet

        Returns:
            QuerySet of companies with addresses, phones and emails.
        """
        context = super(CompanyUpdate, self).get_context_data(**kwargs)
        context["address_form"] = AddressFormSet(instance=get_object_or_404(Company, pk=self.kwargs['pk']))
        context["phone_form"] = PhoneFormSet(instance=get_object_or_404(Company, pk=self.kwargs['pk']))
        context["email_form"] = EmailFormSet(instance=get_object_or_404(Company, pk=self.kwargs['pk']))
        return context



class ProjectCreate(PermissionRequiredMixin, CreateView):
    """A class used to create a project

    Attributes:
        model (class): Database's table
        fields (list): List of fields.
        permission_required (str): Page access for manager and administrators
    """
    model = Project
    fields = ['company', 'name', 'description', 'date_start', 'date_finish', 'cost']
    permission_required = 'crm_app.add_project'
    


class ProjectUpdate(PermissionRequiredMixin, UpdateView):
    """A class used to update a project

    Attributes:
        model (class): Database's table
        fields (list): List of fields.
        permission_required (str): Page access for manager and administrators
    """
    model = Project
    fields = ['company', 'name', 'description', 'date_start', 'date_finish', 'cost']
    permission_required = 'crm_app.change_project'


class MessageCreate(PermissionRequiredMixin, CreateView):
    """A class used to create a message

    Attributes:
        model (class): Database's table
        fields (list): List of fields.
        permission_required (str): Page access for manager and administrators
    """
    model = Message
    fields = ['project', 'description', 'circulation_channel', 'rating']
    permission_required = 'crm_app.add_message'
    


class MessageUpdate(PermissionRequiredMixin, UpdateView):
    """A class used to update a project

    Attributes:
        model (class): Database's table
        fields (list): List of fields.
        permission_required (str): Page access for manager and administrators
    """
    model = Message
    fields = ['project', 'description', 'circulation_channel', 'rating']
    permission_required = 'crm_app.change_message'


class UsersMessageListView(PermissionRequiredMixin, generic.ListView):
    """A class used to represent messages which have been added by the manager

    Attributes:
        template_name (str): Name of html template for rendering
        permission_required (str): Page access for manager and administrators
    """
    template_name = 'crm_app/users_message_list.html'
    permission_required = 'crm_app.view_message'

    def get_queryset(self):
        """Overriding QuerySet

        Returns:
            QuerySet of messages.
            Can be sorted and filtered.
        """
        return Message.objects.filter(manager=self.request.user).\
        order_by(self.request.GET.get('orderby', 'date_time')).\
        filter(description__contains=self.request.GET.get('filter', ''))

   