from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Note(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=150, null=False)
    done = models.BooleanField(default=False)
    updated_at = models.DateField(null=False, auto_now=True)
    created_at = models.DateField(null=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        ordering = ['-done']


class NoteTag(models.Model):
    tag = models.CharField(max_length=20)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    updated_at = models.DateField(null=False, auto_now=True)
    
    def __str__(self):
        return self.tag
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['-updated_at']
