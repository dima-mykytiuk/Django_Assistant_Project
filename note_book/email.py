from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_email_about_new_note(user, note_name, description, tags):
    context = {
        'user': user,
        'note_name': note_name,
        'description': description,
        'tags': tags,
    }
    email_body = render_to_string('email_notifications/email_about_new_note.html', context)
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
        'mail': mail,
        'note_name': note_name
    }
    email_body = render_to_string('email_notifications/email_about_delete_note.html', context)
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
        'mail': mail,
        'note_name': note_name
    }
    email_body = render_to_string('email_notifications/email_about_adding_tag.html', context)
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
        'mail': mail,
        'note_name': note_name,
        'tag': tag
    }
    email_body = render_to_string('email_notifications/email_about_delete_tag.html', context)
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
        'mail': mail,
        'new_name': new_name
    }
    email_body = render_to_string('email_notifications/email_about_change_note_name.html', context)
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
        'mail': mail,
        'note_name': note_name
    }
    email_body = render_to_string('email_notifications/email_about_change_desc.html', context)
    email = EmailMessage(
        'Change note description',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_change_status(user, mail, note_name, status):
    context = {
        'user': user,
        'mail': mail,
        'note_name': note_name,
        'status': status,
    }
    email_body = render_to_string('email_notifications/email_about_change_status.html', context)
    email = EmailMessage(
        'Change note status',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)
