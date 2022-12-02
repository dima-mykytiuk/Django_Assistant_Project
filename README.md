# Web Assistant

This project uses the following technologies:
1. Django<br />
2. PostgresDB<br />
3. Celery<br />
4. RabbitMQ<br />
5. Django Rest Framework<br />


This web application has full user authorization with email confirmation. The functionality of this project can be divided into 3 applications:<br />
1. Contact book where the user can store and edit data about his contacts:
- Name<br />
- Phones<br />
- Address<br />
- Birthday<br />
- Mail<br />
2. Notes where the user can create and edit note data:
- Note title<br />
- Tags<br />
- Description<br />
- Status<br />
3. File manager where the user can upload/download files.

With Celery and RabbitMQ, this project implemented an email notification that informs the user about his every action on the website.<br />
Also in this project, the Django Rest Framework functionality is implemented, access to which only the administrator has access.

Small Demo of project: https://www.youtube.com/watch?v=Z2Alz_LjSwk

### Installation
1. You need to have pre installed IDE and Docker
2. Create new project and clone project from git in your IDE
3. You need to have google mail with 2-FA to create app password to send notifications:
  - Login to your Gmail account
  - Click on manage your account
  - Select the security option and enable the two factor authentication (2-FA)
  - Once the 2-FA option is available, you now have the option to create an app password
  - Create app password following this instruction [Link](https://support.google.com/mail/answer/185833?hl=en)
4. Open .env file in project root and fill in the file like this example:<br />
DB_NAME=WebAssistant<br />
DB_USER=postgres<br />
DB_PASS=password<br />
DB_HOST=db<br />
DB_PORT=5432<br />
ALLOWED_HOSTS=*<br />
SECRET_KEY=testkey<br />
EMAIL_FROM_USER=testemail@gmail.com<br />
EMAIL_HOST_PASSWORD=app_password<br />
CELERY_BROKER_URL=amqp://guest:guest@RabbitMQ_Server:5672<br />
5. Open in terminal project root where docker-compose.yml and paste this command: docker-compose build.
6. Wait when docker-compose build will be finished and paste next command: docker-compose up.
7. Now you can see that project is running and it is appear in docker application where u can start/stop server in future.
8. And you can go in your browser in path: 127.0.0.1:8000 and use project. <br />
Here is Video Example with all this steps to run this project: <br />
... To be continued!

### Screenshots
![1](https://user-images.githubusercontent.com/39094042/205227709-7db97604-b45d-4ff6-9420-83b9192e516f.jpg)
![2022-12-02 08 09 31](https://user-images.githubusercontent.com/39094042/205227723-82ddd7d0-984a-48d3-acbd-0391a0993891.jpg)
![2022-12-02 08 10 00](https://user-images.githubusercontent.com/39094042/205227784-526f8249-e1a0-411e-bd4e-4bc68dfc258e.jpg)
![2022-12-02 08 09 38](https://user-images.githubusercontent.com/39094042/205227741-8efa0d13-d102-4dc6-bd2a-3afd2e480ca3.jpg)
![2022-12-02 08 09 44](https://user-images.githubusercontent.com/39094042/205227759-ec0969a9-3628-4497-b333-6cee9392bcef.jpg)
![2022-12-02 08 09 53](https://user-images.githubusercontent.com/39094042/205227769-b6434c3d-9382-4a2e-a986-6f24594c1672.jpg)
![2022-12-02 08 10 07](https://user-images.githubusercontent.com/39094042/205227796-4b3c9580-4248-4d0c-9d04-a58b64a939b1.jpg)
