from django.contrib import admin
from authApp.models.user import User
from authApp.models.account import Account

# Register your models here.
admin.site.register(User)
admin.site.register(Account)