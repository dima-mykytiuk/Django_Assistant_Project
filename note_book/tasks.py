from MyAssistantProject.celery import app

from celery.utils.log import get_task_logger

from note_book.email import send_email_about_change_status, send_email_about_new_note, send_email_about_delete_note, \
    send_email_about_adding_tag, send_email_about_delete_tag, send_email_about_change_note_name, \
    send_email_about_change_desc

logger = get_task_logger(__name__)


@app.task(name='send_about_new_note')
def send_about_new_note(user, note_name):
    logger.info("Sent email")
    return send_email_about_new_note(user, note_name)


@app.task(name='send_delete_note')
def send_delete_note(user, mail, note_name):
    logger.info("Sent email")
    return send_email_about_delete_note(user, mail, note_name)


@app.task(name='send_add_tag')
def send_add_tag(user, mail, note_name):
    logger.info("Sent email")
    return send_email_about_adding_tag(user, mail, note_name)


@app.task(name='send_delete_tag')
def send_delete_tag(user, mail, note_name, tag):
    logger.info("Sent email")
    return send_email_about_delete_tag(user, mail, note_name, tag)


@app.task(name='send_change_note_name')
def send_change_note_name(user, mail, new_name):
    logger.info("Sent email")
    return send_email_about_change_note_name(user, mail, new_name)


@app.task(name='send_change_note_desc')
def send_change_note_desc(user, mail, note_name):
    logger.info("Sent email")
    return send_email_about_change_desc(user, mail, note_name)


@app.task(name='send_change_note_status')
def send_change_note_status(user, mail, note_name, status):
    logger.info("Sent email")
    return send_email_about_change_status(user, mail, note_name, status)
