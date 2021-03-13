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
    model = Company
    paginate_by = 12
    template_name = 'index.html'

    # @login_required(login_url='/accounts/login/')
    # def get_queryset(self):
    #     pass

    def get_ordering(self):
        ordering = self.request.GET.get('orderby')
        print(ordering)
        return ordering


class CompanyDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Company
    permission_required = 'crm_app.view_company'


class ProjectDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Project
    permission_required = 'crm_app.view_project'


class MessageDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Message
    permission_required = 'crm_app.view_message'



class ProjectListView(PermissionRequiredMixin, generic.ListView):
    template_name = 'crm_app/project_list.html'
    permission_required = 'crm_app.view_project'
    def get_queryset(self):
        self.company = get_object_or_404(Company, pk=self.kwargs['pk'])
        return Project.objects.filter(company=self.company).order_by(self.request.GET.get('orderby', 'name'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['pk'] = self.kwargs['pk']
        return context

    # def get_ordering(self):
    #     ordering = self.request.GET.get('orderby')
    #     # print(ordering)
    #     return ordering


class MessageCompanyListView(PermissionRequiredMixin, generic.ListView):
    template_name = 'crm_app/comp_message_list.html'
    permission_required = 'crm_app.view_message'

    def get_queryset(self):
        self.company = get_object_or_404(Company, pk=self.kwargs['pk'])
        return Message.objects.filter(project__company=self.company).\
        order_by(self.request.GET.get('orderby', 'date_time')).\
        filter(description__contains=self.request.GET.get('filter', ''))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['pk'] = self.kwargs['pk']
        return context


class MessageProjectListView(PermissionRequiredMixin, generic.ListView):
    template_name = 'crm_app/proj_message_list.html'
    permission_required = 'crm_app.view_message'

    def get_queryset(self):
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return Message.objects.filter(project=self.project).\
        order_by(self.request.GET.get('orderby', 'date_time')).\
        filter(description__contains=self.request.GET.get('filter', ''))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        context['pk'] = self.kwargs['pk']
        return context


class CompanyCreate(PermissionRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    permission_required = 'crm_app.add_company'

    # fields = ['name', 'director', 'description']

    def get_context_data(self, **kwargs):
        context = super(CompanyCreate, self).get_context_data(**kwargs)
        context["address_form"] = AddressFormSet()
        context["phone_form"] = PhoneFormSet()
        context["email_form"] = EmailFormSet()
        return context


    # def get(self, request, *args, **kwargs):
    #     """
    #     Handles GET requests and instantiates blank versions of the form
    #     and its inline formsets.
    #     """
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     address_form = AddressFormSet()
    #     phone_form = PhoneFormSet()
    #     email_form = EmailFormSet()
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               address_form=address_form,
    #                               phone_form=phone_form,
    #                               email_form=email_form))

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handles POST requests, instantiating a form instance and its inline
    #     formsets with the passed POST variables and then checking them for
    #     validity.
    #     """
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     address_form = AddressFormSet(self.request.POST)
    #     phone_form = PhoneFormSet(self.request.POST)
    #     email_form = EmailFormSet(self.request.POST)
    #     if (form.is_valid() and address_form.is_valid() and
    #         phone_form.is_valid() and email_form.is_valid()):
    #         return self.form_valid(form, address_form, phone_form, email_form)
    #     else:
    #         return self.form_invalid(form, address_form, phone_form, email_form)

    # def form_valid(self, form, address_form, phone_form, email_form):
    #     """
    #     Called if all forms are valid. Creates a Recipe instance along with
    #     associated Ingredients and Instructions and then redirects to a
    #     success page.
    #     """
    #     self.object = form.save()
    #     address_form.instance = self.object
    #     address_form.save()
    #     phone_form.instance = self.object
    #     phone_form.save()
    #     email_form.instance = self.object
    #     email_form.save()
    #     return HttpResponseRedirect(self.get_success_url())

    # def form_invalid(self, form, address_form, phone_form, email_form):
    #     """
    #     Called if a form is invalid. Re-renders the context data with the
    #     data-filled forms and errors.
    #     """
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               address_form=address_form,
    #                               phone_form=phone_form,
    #                               email_form=email_form))



class CompanyUpdate(PermissionRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    permission_required = 'crm_app.change_company'
    # fields = ['name', 'director', 'description']

    # def get_context_data(self, **kwargs):
    #     context = super(CompanyUpdate, self).get_context_data(**kwargs)
    #     context["address_form"] = AddressFormSet(instance=get_object_or_404(Company, pk=self.kwargs['pk']))
    #     context["phone_form"] = PhoneFormSet(instance=get_object_or_404(Company, pk=self.kwargs['pk']))
    #     context["email_form"] = EmailFormSet(instance=get_object_or_404(Company, pk=self.kwargs['pk']))
    #     return context

    # def get_success_url(self):
    #     return reverse_lazy('projects')

    # def get_context_data(self, **kwargs):
    #     context = super(CompanyUpdate, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['form'] = CompanyForm(self.request.POST, instance=self.object)
    #         context["address_form"] = AddressFormSet(self.request.POST, instance=self.object)
    #         context["phone_form"] = PhoneFormSet(self.request.POST, instance=self.object)
    #         context["email_form"] = EmailFormSet(self.request.POST, instance=self.object)
    #     else:
    #         context['form'] = CompanyForm(instance=self.object)
    #         context["address_form"] = AddressFormSet(instance=self.object)
    #         context["phone_form"] = PhoneFormSet(instance=self.object)
    #         context["email_form"] = EmailFormSet(instance=self.object)
    #     return context

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     formset = MaterialRequestFormset(self.request.POST, instance=self.object)
    #     if (form.is_valid() and formset.is_valid()):
    #         return self.form_valid(form, formset)
    #     else:
    #         return self.form_invalid(form, formset)

    # def form_valid(self, form, formset):
    #     self.object = form.save()
    #     formset.instance = self.object
    #     formset.save()
    #     return HttpResponseRedirect(self.get_success_url())

    # def form_invalid(self, form, formset):
    #     return self.render_to_response(self.get_context_data(form=form, formset=formset))



    # model = Company
    # form_class = CompanyForm
    # fields = ['name', 'director', 'description']

    # def get(self, request, *args, **kwargs):
    #     """
    #     Handles GET requests and instantiates blank versions of the form
    #     and its inline formsets.
    #     """
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     address_form = AddressFormSet()
    #     phone_form = PhoneFormSet()
    #     email_form = EmailFormSet()
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               address_form=address_form,
    #                               phone_form=phone_form,
    #                               email_form=email_form))

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handles POST requests, instantiating a form instance and its inline
    #     formsets with the passed POST variables and then checking them for
    #     validity.
    #     """
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     address_form = AddressFormSet(self.request.POST)
    #     phone_form = PhoneFormSet(self.request.POST)
    #     email_form = EmailFormSet(self.request.POST)
    #     if (form.is_valid() and address_form.is_valid() and
    #         phone_form.is_valid() and email_form.is_valid()):
    #         return self.form_valid(form, address_form, phone_form, email_form)
    #     else:
    #         return self.form_invalid(form, address_form, phone_form, email_form)

    # def form_valid(self, form, address_form, phone_form, email_form):
    #     """
    #     Called if all forms are valid. Creates a Recipe instance along with
    #     associated Ingredients and Instructions and then redirects to a
    #     success page.
    #     """
    #     self.object = form.save()
    #     address_form.instance = self.object
    #     address_form.save()
    #     phone_form.instance = self.object
    #     phone_form.save()
    #     email_form.instance = self.object
    #     email_form.save()
    #     return HttpResponseRedirect(self.get_success_url())

    # def form_invalid(self, form, address_form, phone_form, email_form):
    #     """
    #     Called if a form is invalid. Re-renders the context data with the
    #     data-filled forms and errors.
    #     """
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               address_form=address_form,
    #                               phone_form=phone_form,
    #                               email_form=email_form))



class ProjectCreate(PermissionRequiredMixin, CreateView):
    model = Project
    fields = ['company', 'name', 'description', 'date_start', 'date_finish', 'cost']
    permission_required = 'crm_app.add_project'
    


class ProjectUpdate(PermissionRequiredMixin, UpdateView):
    model = Project
    fields = ['company', 'name', 'description', 'date_start', 'date_finish', 'cost']
    permission_required = 'crm_app.change_project'


class MessageCreate(PermissionRequiredMixin, CreateView):
    model = Message
    fields = ['project', 'description', 'circulation_channel', 'rating']
    permission_required = 'crm_app.add_message'
    


class MessageUpdate(PermissionRequiredMixin, UpdateView):
    # def test_func(self):
    #     return self.request.user.user_name == 
    model = Message
    fields = ['project', 'description', 'circulation_channel', 'rating']
    permission_required = 'crm_app.change_message'


class UsersMessageListView(PermissionRequiredMixin, generic.ListView):
    template_name = 'crm_app/users_message_list.html'
    permission_required = 'crm_app.view_message'

    def get_queryset(self):
        return Message.objects.filter(manager=self.request.user).\
        order_by(self.request.GET.get('orderby', 'date_time')).\
        filter(description__contains=self.request.GET.get('filter', ''))

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['project'] = self.project
    #     context['pk'] = self.kwargs['pk']
    #     return context

