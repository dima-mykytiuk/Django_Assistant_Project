from rest_framework import serializers
from .models import Note, NoteTag


class NoteSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Note
        fields = '__all__'


class NoteTagSerializer(serializers.ModelSerializer):
    note = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Note.objects.all()
    )
            
    class Meta:
        model = NoteTag
        fields = '__all__'
