from rest_framework import serializers
from .models import Note, NoteTag


class NoteTagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    def validate(self, data):
        if len(data['tag']) > 20:
            raise serializers.ValidationError("Tag length is maximum 20 characters")
        return data
    
    class Meta:
        model = NoteTag
        fields = ('id', 'tag')


class NoteSerializer(serializers.ModelSerializer):
    tags = NoteTagSerializer(many=True)
    
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        note = Note.objects.create(**validated_data)
        for tag in tags:
            NoteTag.objects.create(note=note, tag=tag.get('tag'))
        return note
    
    def update(self, instance, validated_data):
        note_tag = [tag.tag for tag in NoteTag.objects.filter(note_id=instance.id)]
        tags = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.done = validated_data.get('done', instance.done)
        instance.save()
        list_of_tags = [tag['tag'] for tag in tags]
        for tag in tags:
            if "id" in tag.keys():
                note = NoteTag.objects.get(id=tag["id"])
                note.tag = tag.get('tag', note.tag)
                note.save()
            else:
                if tag.get('tag') in note_tag:
                    raise serializers.ValidationError("This tag is already on this note")
                else:
                    note_tag.append(tag.get('tag'))
                    NoteTag.objects.create(note=instance, tag=tag.get('tag'))
        if len(note_tag) > len(tags):
            for tag in note_tag:
                if tag not in list_of_tags:
                    NoteTag.objects.get(tag=tag).delete()
        return instance

    class Meta:
        model = Note
        fields = ('id', 'name', 'description', 'done', 'tags', 'user')

    def validate(self, data):
        if len(data['description']) > 150:
            raise serializers.ValidationError("Note description length is maximum 150 characters")
        if len(data['tags']) > 4:
            raise serializers.ValidationError("Maximum amount of tags is 4")
        if len(data['name']) > 50:
            raise serializers.ValidationError("Note name length is maximum 15 characters")
        return data

