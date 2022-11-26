from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_email_about_new_note(user, note_name):
    context = {
        'user': user,
        'message': f"You successfully added note '{note_name}' in your note list",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
    email = EmailMessage(
        'New Note',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[user],
    )
    return email.send(fail_silently=False)


def send_email_about_delete_note(user, mail, note_name):
    context = {
        'user': user,
        'message': f"You successfully deleted note {note_name} from your note list!",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
    email = EmailMessage(
        'Delete Note',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_adding_tag(user, mail, note_name):
    context = {
        'user': user,
        'message': f"You successfully added tag to note {note_name}!",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
    email = EmailMessage(
        'Add Tag',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_delete_tag(user, mail, note_name, tag):
    context = {
        'user': user,
        'message': f"You successfully deleted tag {tag} from note {note_name} in your note book!",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
    email = EmailMessage(
        'Delete Tag',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_change_note_name(user, mail, new_name):
    context = {
        'user': user,
        'message': f"You successfully changed note name in your note book, new note name: {new_name}!",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
    email = EmailMessage(
        'Change note name',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_change_desc(user, mail, note_name):
    context = {
        'user': user,
        'message': f"You successfully changed description for note {note_name} in your note book!",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
    email = EmailMessage(
        'Change note description',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_change_status(user, mail, note_name, status):
    status = 'Completed' if status else 'Not completed'
    context = {
        'user': user,
        'message': f"You successfully changed note {note_name} status to {status} in your note book!",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
    email = EmailMessage(
        'Change note status',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)
