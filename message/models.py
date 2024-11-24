from django.db import models
from django.db.models import JSONField

# Create your models here.
# class Messages(models.Model):
#     message = models.TextField()
#     sender = models.CharField(max_length=50)
#     receiver = models.CharField(max_length=50)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.sender + self.receiver + self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    

class Messages(models.Model):
   id = models.CharField(max_length=255, primary_key=True)
   from_field = models.CharField(max_length=255, blank=True)
   to = models.CharField(max_length=255, blank=True)
   author = models.CharField(max_length=255, blank=True)
   pushname = models.CharField(max_length=255, blank=True)
   ack = models.CharField(max_length=255, blank=True)
   type = models.CharField(max_length=255, blank=True)
   body = models.TextField(blank=True)
   media = models.CharField(max_length=255, blank=True)
   fromMe = models.BooleanField(blank=True)
   isSelf = models.BooleanField(blank=True)
   isForwarded = models.BooleanField(blank=True)
   isMentioned = models.BooleanField(blank=True)
#    dictionary field
   quotedMsg = models.JSONField(blank=True)
   mentionedIds = models.JSONField(blank=True)
   time = models.BigIntegerField(blank=True)
    
class Whatsapp_Message(models.Model):
    message_id =  models.CharField(max_length=100)
    profile_name = models.CharField(max_length=100, default="Me")
    message_type = models.CharField(max_length=30, default="text")
    _from = models.CharField(max_length=50)
    body = models.TextField()
    to = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message received from {self._from} to {self.to}"

class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number + self.timestamp.strftime("%Y-%m-%d %H:%M:%S")