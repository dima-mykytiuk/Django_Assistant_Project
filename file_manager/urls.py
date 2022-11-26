from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings

from file_manager.views import IndexView, FileManagerView, ShowByCategoryView, DeleteFileView, UploadFileView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('file_manager/', FileManagerView.as_view(), name='file_manager'),
    path('file_manager/upload/', UploadFileView.as_view(), name='upload'),
    path('file_manager/delete_file/<int:pk>', DeleteFileView.as_view(), name='delete_file'),
    path('file_manager/show_by_category/<category_id>', ShowByCategoryView.as_view(), name='show_by_category'),
    url(r'^download/(?P<path>.*)$/', serve, {'document_root': settings.MEDIA_ROOT}),
]
