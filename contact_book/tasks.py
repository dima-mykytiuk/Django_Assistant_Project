from MyAssistantProject.celery import app

from celery.utils.log import get_task_logger

from .email import send_email_about_contact, send_email_about_delete, send_email_about_adding_phone, \
    send_email_about_delete_phone, send_email_about_change_name, send_email_about_change_email, \
    send_email_about_change_birthday, send_email_about_change_address

logger = get_task_logger(__name__)


@app.task(name='send_add_contact_email')
def send_add_contact_email(user, name, email, phone):
    logger.info("Sent email")
    return send_email_about_contact(user, name, email, phone)


@app.task(name='send_delete_contact')
def send_delete_contact(user, mail, contact_name):
    logger.info("Sent email")
    return send_email_about_delete(user, mail, contact_name)


@app.task(name='send_add_phone')
def send_add_phone(user, mail, contact):
    logger.info("Sent email")
    return send_email_about_adding_phone(user, mail, contact)


@app.task(name='send_delete_phone')
def send_delete_phone(user, mail, contact):
    logger.info("Sent email")
    return send_email_about_delete_phone(user, mail, contact)


@app.task(name='send_change_name')
def send_change_name(user, mail):
    logger.info("Sent email")
    return send_email_about_change_name(user, mail)


@app.task(name='send_change_email')
def send_change_email(user, mail, contact):
    logger.info("Sent email")
    return send_email_about_change_email(user, mail, contact)


@app.task(name='send_change_birthday')
def send_change_birthday(user, mail, contact):
    logger.info("Sent email")
    return send_email_about_change_birthday(user, mail, contact)


@app.task(name='send_change_address')
def send_change_address(user, mail, contact):
    logger.info("Sent email")
    return send_email_about_change_address(user, mail, contact)
