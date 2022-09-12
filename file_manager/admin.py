from django.contrib import admin
from .models import FileManager, FileType

# Register your models here.
admin.site.register(FileManager)
admin.site.register(FileType)
