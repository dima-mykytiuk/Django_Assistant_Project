import os.path

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def user_directory_path(instance,  filename):
    return f'user_{instance.user.username}/{filename}'


class FileType(models.Model):
    file_type = models.CharField(max_length=20)

    def __str__(self):
        return self.file_type
    
    @classmethod
    def create(cls, file_type):
        new_category = cls(file_type=file_type)
        return new_category


class FileManager(models.Model):
    file_name = models.FileField(upload_to=user_directory_path)
    file_type = models.ForeignKey(FileType, on_delete=models.DO_NOTHING)
    uploaded_at = models.DateField(null=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        self.file_name.delete()
        super().delete(*args, **kwargs)
        
    def filename(self):
        return os.path.basename(self.file_name.name)