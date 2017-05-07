from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from watson import search as watson
from .models import Person,Student,Faculty,Course,Project
from .models import Request,StudentRequest,FacultyRequest,CourseRequest,ProjectRequest
from .forms import StudentForm,FacultyForm,CourseForm,ProjectForm,CourseRequestForm,ProjectRequestForm
from .templatetags.tags import has_group

# Create a Moderator Group
MODERATOR_GROUP_NAME = 'Moderator'
moderator_group,created = Group.objects.get_or_create(name=MODERATOR_GROUP_NAME)


def index(request):
    return HttpResponseRedirect(reverse('home'))

@login_required
def search(request):
    context = {}
    if request.method == 'POST':
        query = request.POST['query']
        search_results = watson.search(query)
        student_results = []
        faculty_results = []
        course_results = []
        project_results = []
        for result in search_results:
            className = result.object.__class__.__name__
            if result.object.visible is not None and result.object.visible == False:
                continue
            if className == 'Student':
                result.url = reverse('student', kwargs={'entryNumber': result.object.entryNumber})
                result.heading = result.object.name
                student_results.append(result)
            elif className == 'Faculty':
                result.url = reverse('faculty', kwargs={'id': result.object.id})
                result.heading = result.object.name
                faculty_results.append(result)
            elif className == 'Course':
                result.url = reverse('course', kwargs={'courseCode': result.object.code})
                result.heading = result.object.name
                course_results.append(result)
            elif className == 'Project':
                result.url = reverse('project', kwargs={'projectId': result.object.id})
                result.heading = result.object.title
                project_results.append(result)

        results = [('Students', student_results), ('Faculty', faculty_results), ('Courses', course_results), ('Projects', project_results)]
        context['results'] = results
        context['query'] = query
        context['num_results'] = sum([len(x) for _,x in results])

    return render(request, 'search.html', context)

@login_required
def student(request, entryNumber):
    context = {}
    try:
        student = Student.objects.get(pk=entryNumber)
        context['student'] = student
        context['projects'] = student.projects.all()
        context['form'] = StudentForm(instance=student)
    except:
        context['error'] = "No student with entry number %s" % entryNumber

    return render(request, 'student.html', context)
        
@login_required
def faculty(request, id):
    context = {}
    try:
        faculty = Faculty.objects.get(pk=id)
        context['faculty'] = faculty
        context['courses'] = faculty.courses.all()
        context['projects'] = faculty.projects.all()
        context['form'] = FacultyForm(instance=faculty)
    except:
        context['error'] = "No faculty with id %s" % id
    
    return render(request, 'faculty.html', context)

@login_required
def course(request, courseCode):
    context = {}
    try:
        course = Course.objects.get(code__iexact=courseCode)
        context['course'] = course
        context['form'] = CourseForm(instance=course)
    except Course.DoesNotExist:
        context['error'] = "No course with code %s" % courseCode
    
    return render(request, 'course.html', context)

@login_required
def project(request, projectId):
    context = {}
    try:
        project = Project.objects.get(pk=projectId)
        context['project'] = project
        context['form'] = ProjectForm(instance=project)
    except:
        context['error'] = "No project with ID %s" % projectId

    return render(request, 'project.html', context)

@login_required
def add_student(request):
    if request.method == "POST":
        kwargs = request.POST.copy()
        kwargs['ptype'] = 'Student'
        form = StudentForm(kwargs)
        if form.is_valid():
            student = form.save(commit=False)
            student.visible = False
            student.save()
            studentRequest = StudentRequest(user=request.user, status='Pending', data=student)
            studentRequest.save()
            return HttpResponseRedirect(reverse('request_submitted'))
    else:
        form = StudentForm()
    
    # make the ptype field hidden and initialize it later
    form.fields['ptype'].widget = forms.HiddenInput()
    context = {'form': form, 'model_name': 'Student'}
    return render(request, 'add_page.html', context)

@login_required
def add_faculty(request):
    if request.method == "POST":
        kwargs = request.POST.copy()
        kwargs['ptype'] = 'Faculty'
        form = FacultyForm(kwargs)
        if form.is_valid():
            faculty = form.save(commit=False)
            faculty.visible = False
            faculty.save()
            facultyRequest = FacultyRequest(user=request.user, status='Pending', data=faculty)
            facultyRequest.save()
            return HttpResponseRedirect(reverse('request_submitted'))
    else:
        form = FacultyForm()
    
    # make the ptype field hidden and initialize it later
    form.fields['ptype'].widget = forms.HiddenInput()
    context = {'form': form, 'model_name': 'Faculty'}
    return render(request, 'add_page.html', context)

@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseRequestForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.visible = False
            course.save()
            form.save_m2m() # required beacuase commit=False and course has m2m field
            courseRequest = CourseRequest(user=request.user, status='Pending', data=course)
            courseRequest.save()
            return HttpResponseRedirect(reverse('request_submitted'))
    else:
        form = CourseRequestForm()
    
    context = {'form': form, 'model_name': 'Course'}
    return render(request, 'add_page.html', context)

@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectRequestForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.visible = False
            project.save()
            form.save_m2m() # required beacuase commit=False and project has m2m fields
            projectRequest = ProjectRequest(user=request.user, status='Pending', data=project)
            projectRequest.save()
            return HttpResponseRedirect(reverse('request_submitted'))
    else:
        form = ProjectRequestForm()
    
    context = {'form': form, 'model_name': 'Project'}
    return render(request, 'add_page.html', context)

@login_required
def request_submitted(request):
    return render(request, 'request_submitted.html')

def get_request_heading(userRequest):
    try:
        heading = 'Student: ' + userRequest.studentrequest.data.name
    except Exception as e:
        pass

    try:
        heading = 'Faculty: ' + userRequest.facultyrequest.data.name
    except Exception as e:
        pass

    try:
        heading = 'Course: ' + userRequest.courserequest.data.name
    except Exception as e:
        pass

    try:
        heading = 'Project: ' + userRequest.projectrequest.data.title
    except Exception as e:
        pass

    return heading

@login_required
def my_requests(request):
    user = request.user
    myRequests = user.user_requests.all()
    context = {}
    context['requests'] = {}
    for myRequest in myRequests:
        myRequest.heading = get_request_heading(myRequest)
        myRequest.url = reverse('show_request', kwargs={'requestId': myRequest.pk})
        if myRequest.status not in context['requests']:
            context['requests'][myRequest.status] = []
        context['requests'][myRequest.status].append(myRequest)
        
    context['num_requests'] = len(myRequests)
    return render(request, 'my_requests.html', context)

def get_form_from_user_request(userRequest):
    try:
        form = StudentForm(instance=userRequest.studentrequest.data)
    except Exception as e:
        pass

    try:
        form = FacultyForm(instance=userRequest.facultyrequest.data)
    except Exception as e:
        pass

    try:
        form = CourseRequestForm(instance=userRequest.courserequest.data)
    except Exception as e:
        pass

    try:
        form = ProjectRequestForm(instance=userRequest.projectrequest.data)
    except Exception as e:
        pass

    return form

def get_child_reqeust(parentRequest):
    try:
        childRequest = parentRequest.studentrequest
    except Exception as e:
        pass

    try:
        childRequest = parentRequest.facultyrequest
    except Exception as e:
        pass

    try:
        childRequest = parentRequest.courserequest
    except Exception as e:
        pass

    try:
        childRequest = parentRequest.projectrequest
    except Exception as e:
        pass

    return childRequest

@login_required
def show_request(request, requestId):
    context = {}
    try:
        userRequest = Request.objects.get(pk=requestId)
        context['userRequest'] = userRequest
        context['form'] = get_form_from_user_request(userRequest)

        if request.method == "POST":
            childRequest = get_child_reqeust(userRequest)
            childRequest.data.delete()
            childRequest.request_ptr.delete()
            childRequest.request_ptr.save()
            childRequest.delete()

            return HttpResponseRedirect(reverse('my_requests'))

    except Request.DoesNotExist:
        context['error'] = "No request with id %s" % requestId
    
    return render(request, 'show_request.html', context)

def is_moderator(user):
    return has_group(user, MODERATOR_GROUP_NAME)

@login_required
@user_passes_test(is_moderator, login_url='/')
def moderate(request):
    userRequests = Request.objects.all()
    context = {}
    context['requests'] = {}
    for userRequest in userRequests:
        userRequest.heading = userRequest.user.username + " -> " + get_request_heading(userRequest)
        userRequest.url = reverse('moderate_request', kwargs={'requestId': userRequest.pk})
        if userRequest.status not in context['requests']:
            context['requests'][userRequest.status] = []
        context['requests'][userRequest.status].append(userRequest)
        
    context['num_requests'] = len(userRequests)
    return render(request, 'moderate.html', context)

@login_required
@user_passes_test(is_moderator, login_url='/')
def moderate_request(request, requestId):
    context = {}
    try:
        userRequest = Request.objects.get(pk=requestId)
        context['userRequest'] = userRequest
        context['form'] = get_form_from_user_request(userRequest)

        if request.method == "POST":
            childRequest = get_child_reqeust(userRequest)
            childRequest.feedback = request.POST['feedback']
            moderation_action = request.POST['moderation_action']
            if moderation_action == 'Approve':
                childRequest.data.visible = True
                childRequest.data.save()
                childRequest.status = 'Approved'
                childRequest.save()
            else:
                childRequest.status = 'Rejected'
                childRequest.save()
            return HttpResponseRedirect(reverse('moderate'))

    except Request.DoesNotExist:
        context['error'] = "No request with id %s" % requestId
    
    return render(request, 'moderate_request.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # TODO: authenticate here
        user = authenticate(username=username, password=password)
        if user is not None:
            # user already exist
            print('User already present')
            login(request,user)
        
            return HttpResponseRedirect(reverse('home'))
    
    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))