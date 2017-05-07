from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.contrib.auth.models import User

# Abstract class
class Person(models.Model):
	name = models.CharField(max_length=200, verbose_name="Name")
	email = models.EmailField(max_length=254, verbose_name="E-mail")
	website = models.URLField(verbose_name='Website', blank=True, null=True)

	PERSON_TYPES = [(x,x) for x in ['Student', 'Faculty']]
	ptype = models.CharField(max_length=15, choices=PERSON_TYPES, verbose_name="Type")

	DEPARTMENTS = [(x,x) for x in ['CS','EE', 'HU']]
	department = models.CharField(max_length=50, choices=DEPARTMENTS, verbose_name="Department")

	visible = models.BooleanField(default=True, verbose_name="Visible")

	def __str__(self):
		return self.name

	class Meta:
		abstract = True

class Student(Person):
	entryNumber = models.CharField(max_length=11, primary_key=True, verbose_name="Entry Number")
	programmeName = models.CharField(max_length=15, verbose_name="Programme Name")
	hostel = models.CharField(max_length=15, verbose_name="Hostel", blank=True)

class Faculty(Person):
	researchInterests = models.TextField(verbose_name="Research Interests")


class Course(models.Model):
	codeValidator = RegexValidator(regex=r'[A-Z]{3}\d{3}')
	code = models.CharField(max_length=10, primary_key=True, validators=[codeValidator], verbose_name="Course Code")
	name = models.CharField(max_length=50, verbose_name="Name")
	credits = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Credits")
	ltpValidator = RegexValidator(regex=r'\d-\d-\d')
	LTP = models.CharField(max_length=5, validators=[ltpValidator], verbose_name="LTP")
	contents = models.TextField(verbose_name="Course Contents")
	coordinator = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='coordinated_course', verbose_name="Coordinator", null=True)
	instructors = models.ManyToManyField(Faculty, related_name='courses', verbose_name="Instructors")
	visible = models.BooleanField(default=True, verbose_name="Visible")

	def __str__(self):
		return self.name

class Project(models.Model):
	title = models.CharField(max_length=100, verbose_name="Title")
	description = models.TextField(max_length=2000, verbose_name="Description")
	advisors = models.ManyToManyField(Faculty, related_name='projects', verbose_name="Advisors")
	students = models.ManyToManyField(Student, related_name='projects', verbose_name='Students')
	visible = models.BooleanField(default=True, verbose_name="Visible")

	def __str__(self):
		return self.title

class Request(models.Model):
	user = models.ForeignKey(User, verbose_name="User", related_name="user_requests")
	STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Status")
	feedback = models.TextField(max_length=200, verbose_name="Feedback", blank=True)

	def __str__(self):
		return self.user.username + ":" + self.status

class StudentRequest(Request):
	data = models.ForeignKey(Student, verbose_name="Data", null=True)
	def __str__(self):
		return self.user.username + ': (' + self.data.name + ', ' + self.status + ')' 

class FacultyRequest(Request):
	data = models.ForeignKey(Faculty, verbose_name="Data")
	def __str__(self):
		return self.user.username + ': (' + self.data.name + ', ' + self.status + ')'

class CourseRequest(Request):
	data = models.ForeignKey(Course, verbose_name="Data")
	def __str__(self):
		return self.user.username + ': (' + self.data.name + ', ' + self.status + ')'

class ProjectRequest(Request):
	data = models.ForeignKey(Project, verbose_name="Data")
	def __str__(self):
		return self.user.username + ': (' + self.data.title + ', ' + self.status + ')'