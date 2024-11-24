from django.contrib import admin

from .models import Messages, Whatsapp_Message
# Register your models here.
admin.site.register(Messages)
admin.site.register(Whatsapp_Message)