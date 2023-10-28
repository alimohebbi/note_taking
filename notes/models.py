from django.contrib.auth.models import User
from django.db import models

NOTE_TYPE = [('I', 'Idea'),
             ('T', 'Thought'),
             ('R', 'Reminder')]


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    # create_date = models.DateTimeField("date create")
    # due_date = models.DateTimeField("due date")
    # note_type = models.CharField(max_length=1, choices=NOTE_TYPE)

    def __str__(self):
        return self.title
