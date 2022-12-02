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
... To Be Continue

### Screenshots
![1](https://user-images.githubusercontent.com/39094042/205227709-7db97604-b45d-4ff6-9420-83b9192e516f.jpg)
![2022-12-02 08 09 31](https://user-images.githubusercontent.com/39094042/205227723-82ddd7d0-984a-48d3-acbd-0391a0993891.jpg)
![2022-12-02 08 10 00](https://user-images.githubusercontent.com/39094042/205227784-526f8249-e1a0-411e-bd4e-4bc68dfc258e.jpg)
![2022-12-02 08 09 38](https://user-images.githubusercontent.com/39094042/205227741-8efa0d13-d102-4dc6-bd2a-3afd2e480ca3.jpg)
![2022-12-02 08 09 44](https://user-images.githubusercontent.com/39094042/205227759-ec0969a9-3628-4497-b333-6cee9392bcef.jpg)
![2022-12-02 08 09 53](https://user-images.githubusercontent.com/39094042/205227769-b6434c3d-9382-4a2e-a986-6f24594c1672.jpg)
![2022-12-02 08 10 07](https://user-images.githubusercontent.com/39094042/205227796-4b3c9580-4248-4d0c-9d04-a58b64a939b1.jpg)
