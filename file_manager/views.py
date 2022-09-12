import os
from pathlib import Path

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from .models import FileManager, FileType
from .forms import UploadFile
from django.contrib.auth.decorators import login_required
from .tasks import send_about_upload, send_about_file_delete


# Create your views here.
class IndexView(View):
    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'title': 'Web assistant'})


class FileManagerView(LoginRequiredMixin, View):
    template_name = 'pages/file_manager.html'
    
    def get(self, request, *args, **kwargs):
        if len(FileType.objects.all()) == 0:
            FileType.create("Video").save()
            FileType.create("Audio").save()
            FileType.create("Images").save()
            FileType.create("Archives").save()
            FileType.create("Documents").save()
            FileType.create("Other").save()
        logged_user_id = request.user.id
        files = FileManager.objects.filter(user_id=logged_user_id)
        categories = FileType.objects.all()
        list_of_names = []
        for item in files:
            list_of_names.append(str(item.file_name).split("/")[1])
        context = {
            'files': files,
            'categories': categories,
            'file_name': list_of_names,
        }
        return render(request, template_name=self.template_name, context=context)


class UploadFileView(LoginRequiredMixin, View):
    form_class = UploadFile
    template_name = 'pages/upload.html'
    files_types = {
        'Video': ('.avi', '.mp4', '.mov', '.mkv'),
        'Audio': ('.mp3', '.ogg', '.wav', '.amr'),
        'Images': ('.jpeg', '.png', '.jpg', '.svg'),
        'Archives': ('.zip', '.gz', '.tar'),
        'Documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    }
    
    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        logged_user_id = request.user.id
        file = request.FILES['file']
        file_type = Path(str(file)).suffix.lower()
        for category, extensions in self.files_types.items():
            if file_type in extensions:
                file_category_id = FileType.objects.get(file_type=category).id
                document = FileManager.objects.create(
                    user_id=logged_user_id,
                    file_name=file,
                    file_type_id=file_category_id,
                )
                document.save()
                send_about_upload.delay(self.request.user.username, self.request.user.email, str(file))
                return redirect('file_manager')
        other_ctg_id = FileType.objects.get(file_type='Other').id
        document = FileManager.objects.create(
            user_id=logged_user_id,
            file_name=file,
            file_type_id=other_ctg_id
        )
        document.save()
        send_about_upload.delay(self.request.user.username, self.request.user.email, str(file))
        return redirect('file_manager')


class DeleteFileView(LoginRequiredMixin, DeleteView):
    model = FileManager
    template_name = 'pages/delete_file.html'
    success_url = reverse_lazy('file_manager')

    def delete(self, request, *args, **kwargs):
        file = FileManager.objects.get(pk=self.kwargs['pk'])
        response = super(DeleteFileView, self).delete(request, *args, **kwargs)
        send_about_file_delete.delay(request.user.username, request.user.email, str(file.file_name).split('/')[1])
        return response


class ShowByCategoryView(LoginRequiredMixin, View):
    template_name = 'pages/file_manager.html'

    def get(self, request, *args, **kwargs):
        logged_user_id = request.user.id
        files = FileManager.objects.filter(user_id=logged_user_id, file_type_id=self.kwargs['category_id'])
        categories = FileType.objects.all()
        context = {
            'files': files,
            'categories': categories,
        }
        return render(request, self.template_name, context)
    
    
# @login_required
# def download(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     print(file_path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="name")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404
    