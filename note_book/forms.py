from django import forms
from .models import Note, NoteTag
from .tasks import send_about_new_note, send_add_tag


class AddTag(forms.Form):
    tag = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'tag_form'}))
    
    @staticmethod
    def send_email(user, user_email, note_name):
        send_add_tag.delay(user, user_email, note_name)
    
    def clean(self):

        super(AddTag, self).clean()

        tags = [tg.strip() for tg in self.cleaned_data['tag'].split(',')]

        for this_tag in tags:
            if len(this_tag) > 20:
                self._errors['tag'] = self.error_class(['Tag length is maximum 20 characters'])
                break
        return self.cleaned_data


class AddNote(forms.Form):
    note = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'note_name'}))
    description = forms.CharField(max_length=150, widget=forms.Textarea(attrs={'class': 'note_desc'}))
    tag = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'class': 'tags'}))
    
    def send_email(self, user_email):
        send_about_new_note.delay(user_email, self.cleaned_data['note'], self.cleaned_data['description'], self.cleaned_data['tag'])
        
    def clean(self):

        super(AddNote, self).clean()

        note_to_add = self.cleaned_data['note']
        tags = [tg.strip() for tg in self.cleaned_data['tag'].split(',')]
        description = self.cleaned_data['description']

        if len(note_to_add) > 50:
            self._errors['note'] = self.error_class(['Note name length is maximum 50 characters'])
        if len(description) > 150:
            self._errors['description'] = self.error_class(['Note description length is maximum 150 characters'])
        if len(tags) > 4:
            self._errors['tag'] = self.error_class(['Maximum amount of tags is 4'])
        for this_tag in tags:
            if len(this_tag) > 20:
                self._errors['tag'] = self.error_class(['Tag length is maximum 20 characters'])
                break

        return self.cleaned_data


class ChangeNoteName(forms.ModelForm):
    
    class Meta:
        model = Note
        fields = ('name',)
    
    def clean(self):
        super(ChangeNoteName, self).clean()
        
        new_name = self.cleaned_data['name']
        
        if len(new_name) > 50:
            self._errors['name'] = self.error_class(['Note name length is maximum 50 characters'])
        
        return self.cleaned_data


class ChangeNoteDescription(forms.ModelForm):
    
    class Meta:
        model = Note
        fields = ('description',)
    
    def clean(self):
        super(ChangeNoteDescription, self).clean()
        
        new_description = self.cleaned_data['description']
        
        if len(new_description) > 150:
            self._errors['description'] = self.error_class(['Note description length is maximum 150 characters'])
        
        return self.cleaned_data