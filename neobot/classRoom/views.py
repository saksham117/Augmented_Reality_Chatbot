"""
define your views here
"""
from __future__ import print_function
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# from .forms import CreateClassRoom, JoinClassRoom, CreateAssignmentForm, SubmitAssignmentForm
# from .models import Classroom, StudentClassroom, TeacherClassroom, ClassCodes
# from .models import AssignmentCodes, CreateAssignment, SubmitAssignment
from django.contrib import messages
# for sending email to grant teaccher access
from django.conf import settings
from django.core.mail import send_mail
from .models import Classroom, Assignment
from .forms import Question


from .key import returnKey
import openai
from .gpt import GPT
from .gpt import Example
import pandas as pd

# for generating the class code
# import random
# import string

# # for sorting to do list
# from operator import attrgetter


def index(request):
    """
    returns the home page
    """
    listofClasses = []
    obj = Classroom.objects.all()
    listOfClasses = list(obj)
    return render(request, "index.html", {
                                            'listOfClasses': listOfClasses,
                                                    })



def viewClassRoom(request, classId):
    """
        returns the page containing a list of all assignments that have been assigned
    """
    classroom = Classroom.objects.get(classTeacherMail = classId)
    listOfAssignments = None #stores a list of all the assignments
    try:
        # fetch all the classrooms the teacher teaches
        assignments = classroom.assignment_set.all()
        print(assignments)
        listOfAssignments = list(assignments)
    except:
        print("No assignments exist yet")
    context = {
        'class' : classroom,
        'assignments' : listOfAssignments,
    }
    return render(request, 'classroom/classroomContent.html', context)



def assignment(request, classId, assignmentId):

    if request.method == 'POST':
        gpt = None

        if classId == 'Science_arvind@gmail.com':
            gpt = science()
        elif classId == 'C++_sam@gmail.com':
            gpt = cpp()
        else:
            gpt = dbms()

        fm = Question(request.POST)
        if fm.is_valid():
            prompt = fm.cleaned_data['question']
            output = gpt.get_top_reply(prompt)
            messages.success(request, output)
            return redirect('viewvideo', classId = classId, assignmentId = assignmentId)
    else:
        classroom = Classroom.objects.get(classTeacherMail = classId)
        assignment = Assignment.objects.get(assignmentCode = assignmentId)

        fm = Question()
        context = {
            'assignment' : assignment,
            'form' : fm,
        }

        return render(request, 'classroom/video.html', context)


def science():
    openai.api_key = returnKey()
    gpt = GPT(engine="davinci",
            temperature=0.8,
            output_prefix="",
            max_tokens=400)

    # add some code examples
    """This is where our database will be inserted """

    df = pd.read_csv(r'classRoom/databases/data.csv')
    print(df.columns)
    # print("Given Dataframe :\n", df)

    print("\nIterating over rows using index attribute :\n")
    
    # iterate through each row and select 
    # 'Name' and 'Stream' column respectively.
    for ind in df.index:
        #  print(df['Question'][ind], df['Answer'][ind]) #for testing
        question = str(df['Question'][ind])
        answer = str(df['Answer'][ind])
        gpt.add_example(Example(question, answer))

    # returns all the examples that we have fed to the gpt3 model
    # all_examples = gpt.get_all_examples()
    # print(all_examples)
    print('Science function called')
    return gpt 


def cpp():
    openai.api_key = returnKey()
    gpt = GPT(engine="davinci",
            temperature=0.8,
            output_prefix="",
            max_tokens=400)

    # add some code examples
    """This is where our database will be inserted """

    df = pd.read_csv(r'classRoom/databases/c++.csv', encoding='cp1252')
    print(df.columns)
    # print("Given Dataframe :\n", df)

    print("\nIterating over rows using index attribute :\n")
    
    # iterate through each row and select 
    # 'Name' and 'Stream' column respectively.
    for ind in df.index:
        #  print(df['Question'][ind], df['Answer'][ind]) #for testing
        question = str(df['Question'][ind])
        answer = str(df['Answer'][ind])
        gpt.add_example(Example(question, answer))

    # returns all the examples that we have fed to the gpt3 model
    # all_examples = gpt.get_all_examples()
    # print(all_examples)
    print('C++ function called')
    return gpt 


def dbms():
    openai.api_key = returnKey()
    gpt = GPT(engine="davinci",
            temperature=0.8,
            output_prefix="",
            max_tokens=400)

    # add some code examples
    """This is where our database will be inserted """

    df = pd.read_csv(r'classRoom/databases/dbms.csv', encoding='cp1252')
    print(df.columns)
    # print("Given Dataframe :\n", df)

    print("\nIterating over rows using index attribute :\n")
    
    # iterate through each row and select 
    # 'Name' and 'Stream' column respectively.
    for ind in df.index:
        #  print(df['Question'][ind], df['Answer'][ind]) #for testing
        question = str(df['Question'][ind])
        answer = str(df['Answer'][ind])
        gpt.add_example(Example(question, answer))

    # returns all the examples that we have fed to the gpt3 model
    # all_examples = gpt.get_all_examples()
    # print(all_examples)
    print('DBMS function called')
    return gpt 
