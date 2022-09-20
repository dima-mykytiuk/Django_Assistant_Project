from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from users.views import LogOutView, IndexView, LoginView, RegistrationView, EmailVerify

urlpatterns = [
    path(
        'verify_email/<uidb64>/<token>/',
        EmailVerify.as_view(),
        name='verify_email',
    ),
    path('', IndexView.as_view(), name='index'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
