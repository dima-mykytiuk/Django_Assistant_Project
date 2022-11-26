from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_email_about_upload_file(user, mail, file_name):
    context = {
        'user': user,
        'message': f"You successfully upload file {file_name} !",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
    email = EmailMessage(
        'New file upload',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_file_delete(user, mail, file_name):
    context = {
        'user': user,
        'message': f"You successfully deleted file {file_name} !",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
    email = EmailMessage(
        'Delete File',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)
