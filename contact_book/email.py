from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_email_about_contact(user, name, email, phone):
    context = {
        'user': user,
        'name': name,
        'email': email,
        'phone': phone,
    }
    email_body = render_to_string('email_notifications/add_contact_not.html', context)
    email = EmailMessage(
        'New Contact',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[user],
    )
    return email.send(fail_silently=False)


def send_email_about_delete(user, mail, contact_name):
    context = {
        'user': user,
        'mail': mail,
        'contact_name': contact_name
    }
    email_body = render_to_string('email_notifications/delete_contact_not.html', context)
    email = EmailMessage(
        'Delete Contact',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_adding_phone(user, mail, contact_name):
    context = {
        'user': user,
        'mail': mail,
        'contact_name': contact_name
    }
    email_body = render_to_string('email_notifications/email_about_adding_phone.html', context)
    email = EmailMessage(
        'Add Phone',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_delete_phone(user, mail, contact_name):
    context = {
        'user': user,
        'mail': mail,
        'contact_name': contact_name
    }
    email_body = render_to_string('email_notifications/email_about_delete_phone.html', context)
    email = EmailMessage(
        'Delete Phone',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_change_name(user, mail):
    context = {
        'user': user,
        'mail': mail,
    }
    email_body = render_to_string('email_notifications/email_about_change_name.html', context)
    email = EmailMessage(
        'Change contact name',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_change_address(user, mail, contact):
    context = {
        'user': user,
        'mail': mail,
        'contact': contact
    }
    email_body = render_to_string('email_notifications/email_about_change_address.html', context)
    email = EmailMessage(
        'Change contact address',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_change_birthday(user, mail, contact):
    context = {
        'user': user,
        'mail': mail,
        'contact': contact
    }
    email_body = render_to_string('email_notifications/email_about_change_birthday.html', context)
    email = EmailMessage(
        'Change contact birthday',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)


def send_email_about_change_email(user, mail, contact):
    context = {
        'user': user,
        'mail': mail,
        'contact': contact
    }
    email_body = render_to_string('email_notifications/email_about_change_email.html', context)
    email = EmailMessage(
        'Change contact email',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)