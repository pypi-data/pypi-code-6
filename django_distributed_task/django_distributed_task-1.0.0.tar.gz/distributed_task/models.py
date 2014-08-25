from django.db import models


class Message(models.Model):
    queue = models.CharField(max_length=32, db_index=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)