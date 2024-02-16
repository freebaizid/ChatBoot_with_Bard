from django.db import models




class Conversation(models.Model):
    bot = models.TextField()  
    user = models.TextField()  
    session_id = models.CharField(max_length=800) 