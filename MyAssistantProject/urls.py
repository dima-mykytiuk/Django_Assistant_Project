"""WebAssistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from users.views import CreateUserView
from note_book.views import NotesAPIViewSet
from contact_book.views import ContactsAPIViewSet
from file_manager.views import FileUploadDownloadApiView

router = routers.SimpleRouter()
router.register(r'users', CreateUserView)
router.register(r'notes', NotesAPIViewSet)
router.register(r'contacts', ContactsAPIViewSet)
router.register(r'upload/download', FileUploadDownloadApiView)

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('', include('note_book.urls')),
    path('', include('file_manager.urls')),
    path('', include('contact_book.urls')),
    path('', include('users.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
]
