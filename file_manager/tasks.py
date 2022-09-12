from MyAssistantProject.celery import app

from celery.utils.log import get_task_logger

from .email import send_email_about_upload_file, send_email_about_file_delete

logger = get_task_logger(__name__)


@app.task(name='send_about_upload')
def send_about_upload(user, name, file_name):
    logger.info("Sent email")
    return send_email_about_upload_file(user, name, file_name)


@app.task(name='send_about_file_delete')
def send_about_file_delete(user, mail, file_name):
    logger.info("Sent email")
    return send_email_about_file_delete(user, mail, file_name)
