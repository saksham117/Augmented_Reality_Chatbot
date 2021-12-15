"""
List of Models
"""
from django.db import models
from  embed_video.fields  import  EmbedVideoField


# the field classTeacherMail is a primary key and is formed by concatenating className with
# email id of teacher who created it
class Classroom(models.Model):
    """ List of Classes """
    className = models.CharField(max_length=100)
    courseID = models.CharField(max_length=50)
    teacher =  models.EmailField(max_length=100)
    classTeacherMail = models.CharField(max_length=254, primary_key=True)
    classCode = models.CharField(max_length=10, unique=True)


# model to store all the assignment uploaded as of now
class Assignment(models.Model):
    """ List of Assignments """
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    assignmentCode = models.CharField(max_length=10)
    link = models.URLField()
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)
    video = EmbedVideoField()


