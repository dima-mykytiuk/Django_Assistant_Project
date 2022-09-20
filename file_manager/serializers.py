from rest_framework import serializers
from .models import FileManager, FileType


class FileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file_type = serializers.SlugRelatedField(slug_field='file_type', queryset=FileType.objects.all())
    
    class Meta:
        model = FileManager
        fields = "__all__"
        