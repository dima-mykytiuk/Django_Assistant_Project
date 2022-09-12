from django.contrib import admin

from .models import Note, NoteTag

# Register your models here.
admin.site.register(Note)
admin.site.register(NoteTag)
