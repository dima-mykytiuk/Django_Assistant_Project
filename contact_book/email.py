from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_email_about_contact(user_email, user, name):
    context = {
        'user': user,
        'message': f"You successfully added {name} contact in your contact list",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
    email = EmailMessage(
        'New Contact',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[user_email],
    )
    return email.send(fail_silently=False)


def send_email_about_delete(user, mail, contact_name):
    context = {
        'user': user,
        'message': f"You successfully deleted contact {contact_name} from your contact list!",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
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
        'message': f"You successfully added phone to contact {contact_name} in your contact list",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
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
        'message': f"You successfully deleted phone from contact {contact_name} in your contact list",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
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
        'message': f"You successfully changed name for contact in your contact list!",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
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
        'message': f"You successfully changed address for contact {contact} in your contact list!",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
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
        'message': f"You successfully changed birthday for contact {contact} in your contact list!",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
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
        'message': f"You successfully changed email for contact {contact} in your contact list!",
    }
    email_body = render_to_string('email_notifications/email_notification.html', context)
    email = EmailMessage(
        'Change contact email',
        email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[mail],
    )
    return email.send(fail_silently=False)
