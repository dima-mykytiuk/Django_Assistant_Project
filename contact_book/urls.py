from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import AddContactView, IndexView, PhoneDeleteView, ContactsView, ContactDeleteView, DetailContactView, \
    ChangeAddressView, ChangeBirthdayView, ChangeEmailView, ChangeNameView, AddPhoneView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact_book/', ContactsView.as_view(), name='contact_book'),
    path('contact_book/add_contact/', AddContactView.as_view(), name='add_contact'),
    path('contact_book/detail/delete_contact/<int:pk>', ContactDeleteView.as_view(), name='delete_contact'),
    path('contact_book/detail/<int:contact_id>', DetailContactView.as_view(), name='detail_contact'),
    path('contact_book/change_name/<int:pk>', ChangeNameView.as_view(), name='change_name'),
    path('contact_book/change_birthday/<int:pk>', ChangeBirthdayView.as_view(), name='change_birthday'),
    path('contact_book/add_phone/<contact_id>', AddPhoneView.as_view(), name='add_phone'),
    path('contact_book/detail/<int:contact_id>/delete_phone/<int:pk>', PhoneDeleteView.as_view(), name='delete_phone'),
    path('contact_book/change_email/<int:pk>/', ChangeEmailView.as_view(), name='change_email'),
    path('contact_book/change_address/<int:pk>/', ChangeAddressView.as_view(), name='change_address'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
