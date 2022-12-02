# IMAGE CLASSIFIER WEB APP

This project uses the following technologies:
1. Django<br />
2. PostgresDB<br />
3. Celery<br />
4. RabbitMQ<br />
5. Django Rest Framework<br />


This web application has full user authorization with email confirmation. The functionality of this project can be divided into 3 applications:<br />
1. Contact book where the user can store and edit data about his contacts:<br />
*Name<br />
*Phones<br />
*Address<br />
*Birthday<br />
*Mail<br />
2. Notes where the user can create and edit note data:<br />
*Note title<br />
*tags<br />
*Description<br />
*Status<br />
3. File manager where the user can upload/download files.

Also in this project, the DRF functionality is implemented, access to which only the administrator has access.

### Installation
1. You need to have pre installed IDE and Docker
2. Create new project and clone project from git in your IDE
3. Create .env file in project root and fill in the file like this example:<br />
DB_NAME=ImageClassifier<br />
DB_USER=postgres<br />
DB_PASS=password<br />
DB_HOST=db<br />
DB_PORT=5432<br />
ALLOWED_HOSTS=*<br />
SECRET_KEY=testkey<br />
4. Open in terminal project root where docker-compose.yml and paste this command: docker-compose build.
5. Wait when docker-compose build will be finished and paste next command: docker-compose up.
6. Now you can see that project is running and it is appear in docker application where u can start/stop server in future.
7. And you can go in your browser in path: 127.0.0.1:8000. <br />
