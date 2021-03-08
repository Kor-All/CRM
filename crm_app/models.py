from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class Company(models.Model):
	name = models.CharField('Компания', max_length=200)
	director = models.CharField('Директор', max_length=200)
	description = models.TextField('Описание')

	def __str__(self):
		"""
		String for representing the Model object.
		"""
		return self.name

	def get_absolute_url(self):
		return reverse('company_detail', args=[str(self.id)])

	class Meta:
		verbose_name_plural='Компании'
		verbose_name='Компания'


class Address(models.Model):
	"""docstring for Address"""
	company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, verbose_name='Компания')
	address = models.CharField('Адрес', max_length=200)

	def __str__(self):
		"""
		String for representing the Model object.
		"""
		return self.address

	class Meta:
		verbose_name_plural='Адрес'
		verbose_name='Адрес'


class Phone(models.Model):
	"""docstring for Phone"""
	company =  models.ForeignKey(Company, on_delete=models.CASCADE, null=True, verbose_name='Компания')
	phone_number = models.CharField('Тел.номер', max_length=17, blank=True)

	def __str__(self):
		"""
		String for representing the Model object.
		"""
		return self.phone_number

	class Meta:
		verbose_name_plural='Тел.номер'
		verbose_name='Тел.номер'


class Email(models.Model):
	"""docstring for Email"""
	company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, verbose_name='Компания')
	email =  models.EmailField('Эл.почта')

	def __str__(self):
		"""
		String for representing the Model object.
		"""
		return self.email

	class Meta:
		verbose_name_plural='Эл.почта'
		verbose_name='Эл.почта'
	
		
class Project(models.Model):
	"""docstring for Project"""
	company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, verbose_name='Компания')
	name = models.CharField('Проект', max_length=200)
	description = models.TextField('Описание')
	date_start = models.DateField('Дата начала', default=date.today)
	date_finish = models.DateField('Дата окончания', null=True, blank=True)
	cost = models.DecimalField('Стоимость', max_digits=8, decimal_places=2)

	def __str__(self):
		"""
		String for representing the Model object.
		"""
		return self.name

	def get_absolute_url(self):
		return reverse('project_detail', args=[str(self.id)])

	class Meta:
		verbose_name_plural='Проекты'
		verbose_name='Проект'


class Message(models.Model):
	"""docstring for Message"""
	project = models.ForeignKey(Project, on_delete=models.PROTECT, null=True, verbose_name='Проект')
	manager =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Менеджер')
	description = models.TextField('Описание')
	date_time = models.DateTimeField('Дата и время', auto_now_add=True)
	CHANNEL = (
		('p', 'Звонок по телефону'),
		('e', 'Email'),
		('m', 'Мессенджер'),
		('s', 'Заявка через сайт'),
		('c', 'Инициатива нашей компании')
		)
	circulation_channel = models.CharField('Канал взаимодействия', max_length=1, choices=CHANNEL)
	RATING = (
		('vg', 'Отлично'),
		('g', 'Хорошо'),
		('n', 'Нейтрально'),
		('b', 'Плохо'),
		('vb', 'Очень плохо')

		)
	rating = models.CharField('Оценка', max_length=2, choices=RATING)

	def __str__(self):
		"""
		String for representing the Model object
		"""
		return '%s (%s)' % (self.project.name, self.description[:30])

	def get_absolute_url(self):
		return reverse('message_detail', args=[str(self.id)])

	class Meta:
		verbose_name_plural='Взаимодействия'
		verbose_name='Взаимодействие'


	
		




	
		
	
		
