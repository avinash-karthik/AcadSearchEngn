from django import forms
from ASE.models import Student,Faculty,Course,Project

class StudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ['name', 'ptype', 'entryNumber', 'department', 'programmeName', 'email', 'hostel', 'website']

class FacultyForm(forms.ModelForm):
	class Meta:
		model = Faculty
		fields = ['name', 'ptype', 'department', 'email', 'researchInterests', 'website']

class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ['name', 'code', 'credits', 'LTP', 'contents']
		widgets = {'instructors': forms.CheckboxSelectMultiple}

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['title', 'description']
		widgets = {'advisors': forms.CheckboxSelectMultiple, 'students': forms.CheckboxSelectMultiple}

class CourseRequestForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ['name', 'code', 'credits', 'LTP', 'contents', 'coordinator', 'instructors']
		widgets = {'instructors': forms.CheckboxSelectMultiple}

	def __init__(self, *args, **kwargs):
		super(CourseRequestForm, self).__init__(*args, **kwargs)
		# Limit the choice in request form to only visible entries
		self.fields['instructors'].queryset = Faculty.objects.filter(visible=True)
		self.fields['coordinator'].queryset = Faculty.objects.filter(visible=True)

class ProjectRequestForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['title', 'description', 'students', 'advisors']
		widgets = {'advisors': forms.CheckboxSelectMultiple, 'students': forms.CheckboxSelectMultiple}

	def __init__(self, *args, **kwargs):
		super(ProjectRequestForm, self).__init__(*args, **kwargs)
		# Limit the choice in request form to only visible entries
		self.fields['advisors'].queryset = Faculty.objects.filter(visible=True)
		self.fields['students'].queryset = Student.objects.filter(visible=True)
