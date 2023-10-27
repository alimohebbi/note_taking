from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

# class User(models.Model):
#     name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     email_address = models.EmailField(max_length=200)
#     join_date = models.DateTimeField("date joined")
#     password = models.CharField(max_length=128)
#
#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)
#
#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password)
NOTE_TYPE = [('I', 'Idea'),
             ('T', 'Thought'),
             ('R', 'Reminder')]


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    create_date = models.DateTimeField("date create")
    due_date = models.DateTimeField("due date")
    note_type = models.CharField(max_length=1, choices=NOTE_TYPE)
