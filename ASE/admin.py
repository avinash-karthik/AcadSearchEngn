from django.contrib import admin
from .models import Student,Faculty,Course,Project
from .models import Request,StudentRequest,FacultyRequest,CourseRequest,ProjectRequest

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	filter_horizontal = ('instructors',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	filter_horizontal = ('advisors', 'students')

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Request)
admin.site.register(StudentRequest)
admin.site.register(FacultyRequest)
admin.site.register(CourseRequest)
admin.site.register(ProjectRequest)