from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Note, NoteTag
from .forms import AddTag, AddNote, ChangeNoteName, ChangeNoteDescription


# Create your views here.
from .serializers import NoteSerializer, NoteTagSerializer
from .tasks import send_change_note_name, send_change_note_desc, send_change_note_status, send_delete_note, \
    send_delete_tag


"""API"""


class NotesAPIViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('id')
    serializer_class = NoteSerializer
    permission_classes = (IsAdminUser, )


class Index(View):
    template_name = 'pages/index.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'title': 'Web assistant'})


class NotesView(LoginRequiredMixin, View):
    template_name = 'pages/notes.html'
    note_tags = NoteTag.objects.all()
    context = {
    }
    
    def get(self, request, *args, **kwargs):
        logged_user_id = request.user.id
        all_notes = Note.objects.filter(user_id=logged_user_id)
        note_tags = NoteTag.objects.all()
        self.context.update({'notes': all_notes})
        self.context.update({'tags': note_tags})
        return render(request, self.template_name, context=self.context)
    
    def post(self, request, *args, **kwargs):
        logged_user_id = request.user.id
        all_notes = Note.objects.filter(user_id=logged_user_id)
        all_user_notes_ids = [nt.id for nt in all_notes]
        if 'find_note' in request.POST:
            name = request.POST['find_note']
            self.context.update({'notes': Note.objects.filter(user_id=logged_user_id, name__icontains=name)})
        elif 'find_by_tag' in request.POST:
            notes_with_tags = request.POST['find_by_tag']
            tags = NoteTag.objects.filter(note_id__in=all_user_notes_ids, tag__icontains=notes_with_tags)
            self.context.update({"tags": tags})
            contacts_with_id = []
            for item in tags:
                if item.note_id not in contacts_with_id:
                    contacts_with_id.append(item.note_id)
            valid_notes = []
            for item in contacts_with_id:
                valid_notes.append(Note.objects.get(pk=item))
            self.context.update({'notes': valid_notes})
        return render(request, template_name='pages/notes.html', context=self.context)


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'pages/delete_note.html'
    success_url = reverse_lazy('note_book')
    
    def delete(self, request, *args, **kwargs):
        note = Note.objects.get(pk=self.kwargs['pk'])
        response = super(NoteDeleteView, self).delete(request, *args, **kwargs)
        send_delete_note.delay(request.user.username, request.user.email, note.name)
        return response
    
    def get(self, request, *args, **kwargs):
        contact = Note.objects.get(pk=self.kwargs['pk'])
        if request.user.id == contact.user_id:
            response = super(NoteDeleteView, self).get(request, *args, **kwargs)
            return response
        else:
            return HttpResponse(status=404)


class AddTagView(LoginRequiredMixin, View):
    form_class = AddTag
    template_name = 'pages/add_tag.html'
    context = {
        'form': AddTag(),
    }
    
    def get(self, request, *args, **kwargs):
        note_user_id = Note.objects.get(pk=self.kwargs['note_id']).user_id
        if request.user.id == note_user_id:
            self.context.update({'id_note': self.kwargs['note_id']})
            return render(request, self.template_name, context=self.context)
        else:
            return HttpResponse(status=404)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_tag_value = request.POST['tag'].split(',')
            for tag in new_tag_value:
                NoteTag(tag=tag, note_id=Note.objects.filter(id=self.kwargs['note_id'])[0].id).save()
            note = Note.objects.get(pk=self.kwargs['note_id'])
            form.send_email(self.request.user.username, self.request.user.email, note.name)
            return redirect('detail_note', note_id=self.kwargs['note_id'])
        
        return render(request, self.template_name, {'form': form})


class AddNoteView(LoginRequiredMixin, View):
    form_class = AddNote
    template_name = 'pages/add_note.html'
    
    def get(self, request, *args, **kwargs):
        form = AddNote()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        logged_user_id = request.user.id
        form = self.form_class(request.POST)
        if form.is_valid():
            note = form.cleaned_data['note']
            tags = form.cleaned_data['tag']
            description = form.cleaned_data['description']
            note_to_db = Note(user_id=logged_user_id, name=note, description=description)
            note_to_db.save()
            list_of_tags = tags.split(',')
            for tag in list_of_tags:
                tag_to_db = NoteTag(tag=tag.strip(), note_id=note_to_db.id)
                tag_to_db.save()
            form.send_email(self.request.user.email)
            return redirect('note_book')
        
        return render(request, self.template_name, {'form': form})


class DetailNoteView(LoginRequiredMixin, View):
    notes_model = Note
    tag_model = NoteTag
    
    def get(self, request, *args, **kwargs):
        note_tags = self.tag_model.objects.filter(note_id=self.kwargs['note_id'])
        note = self.notes_model.objects.get(pk=self.kwargs['note_id'])
        n = 35
        chunks = [note.description[i:i + n] for i in range(0, len(note.description), n)]
        if request.user.id == note.user_id:
            context = {
                'id_note': self.kwargs['note_id'],
                'tags': note_tags,
                'note': note,
                'note_description': chunks,
            }
            return render(request, 'pages/detail_note.html', context)
        else:
            return HttpResponse(status=404)


class ChangeNameView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    template_name = 'pages/change_note_name.html'
    form_class = ChangeNoteName
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    def get_success_url(self):
        note_id = self.kwargs['pk']
        note_name = Note.objects.get(pk=note_id).name
        send_change_note_name.delay(self.request.user.username, self.request.user.email, note_name)
        return reverse_lazy('detail_note', kwargs={'note_id': note_id})


class ChangeNoteDescView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    template_name = 'pages/change_note_description.html'
    form_class = ChangeNoteDescription
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    def get_success_url(self):
        note_id = self.kwargs['pk']
        note_name = Note.objects.get(pk=note_id).name
        send_change_note_desc.delay(self.request.user.username, self.request.user.email, note_name)
        return reverse_lazy('detail_note', kwargs={'note_id': note_id})


class ChangeNoteStatusView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    def get(self, request, *args, **kwargs):
        note_id = self.kwargs['pk']
        note = Note.objects.get(pk=note_id)
        note.done = False if note.done else True
        note.save()
        send_change_note_status.delay(self.request.user.username, self.request.user.email, note.name, note.done)
        return reverse_lazy('detail_note', kwargs={'note_id': note_id})


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = NoteTag
    template_name = 'pages/delete_tag.html'
    
    def delete(self, request, *args, **kwargs):
        tag = NoteTag.objects.get(pk=self.kwargs['pk'])
        note_name = Note.objects.get(pk=self.kwargs['note_id']).name
        response = super(TagDeleteView, self).delete(request, *args, **kwargs)
        send_delete_tag.delay(request.user.username, request.user.email, note_name, tag.tag)
        return response
    
    def get(self, request, *args, **kwargs):
        contact = Note.objects.get(pk=self.kwargs['note_id'])
        if request.user.id == contact.user_id:
            response = super(TagDeleteView, self).get(request, *args, **kwargs)
            return response
        else:
            return HttpResponse(status=404)
        
    def get_success_url(self):
        note_id = self.kwargs['note_id']
        return reverse_lazy('detail_note', kwargs={'note_id': note_id})