"""
Register your models here.
basically registering and showing all of our models on the admin portal
"""
from django.contrib import admin
from .models import Classroom, Assignment

class ClassroomAdmin(admin.ModelAdmin):
    """
    Model storing all classes
    """
    list_display = ('className', 'courseID', 'teacher', 'classTeacherMail', 'classCode')
    
class AssignmentAdmin(admin.ModelAdmin):
    """
    Model storing all classes
    """
    list_display = ('title', 'description', 'assignmentCode',
                    'link', 'classroom', 'video',)


# registering the models so that we can access them in admin panel
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Assignment, AssignmentAdmin)

