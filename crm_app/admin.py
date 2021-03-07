from django.contrib import admin
from .models import Company, Address, Phone, Email, Project, Message
# Register your models here.


class AddressInline(admin.TabularInline):
	model = Address
	extra = 0


class PhoneInline(admin.TabularInline):
	model = Phone
	extra = 0


class EmailInline(admin.TabularInline):
	model = Email
	extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	inlines = [AddressInline, PhoneInline, EmailInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	pass


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
	pass


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
	pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	pass
