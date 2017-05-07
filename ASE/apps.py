from django.apps import AppConfig
from watson import search as watson

class ASEConfig(AppConfig):
    name = 'ASE'
    verbose_name = "Academic Search Engine"

    def ready(self):
    	course = self.get_model("Course")
    	watson.register(course)
    	student = self.get_model("Student")
    	watson.register(student)
    	faculty = self.get_model("Faculty")
    	watson.register(faculty)
    	project = self.get_model("Project")
    	watson.register(project)