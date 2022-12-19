# Setup-Django-Docker

This repoistory help me to setup project fast with authentication basd on Knox
DB connection Mysql

## Installation Docker

get docker desktop https://docs.docker.com/get-docker/

## Run Docker File

`$ docker-compose -f docker-compose.yml up -d --build`

> Acceses it on localhost without any port by defualt 80 because of Nginx proxy

## Run Project on Local Machine

To Run project to local machine you should install Poetry as environment

### install poetry

`$ pip install poetry`

### Run Project

```
$ poetry shell
$ python manage.py runserver 8000
$ python manage.py makemigrations
$ python manage.py migrate
```

> Acceses it on localhost with port 8000

# Note

Here some notes about run project:

## Environment

In file .env.example
copy .env.example .env

[1] You will find all the environment variables for Docker file Don't Change Environment variables belongs to Mysql
Just put your values

[2] Don't change value MYSQL_DATABASE_HOST
if you wan't change it go to docker compose file and change the container name of image Mysql

## When Run Pytest

[1] access denied for user 'root'@'localhost' to test_mydatabase  
if your database called Ecoomerce then it will be like test_Ecomerce so change test_mydatabase to test_Ecomerce

### To solve This Issue

```
$ docker exec -it bee-db-1 bash
# mysql -u root -p
Will be ask for password should be in env file `MYSQL_ROOT_PASSWORD`
mysql> GRANT ALL PRIVILEGES ON `test_mydatabase`.* TO 'mysqluser'@'%';
```

Don't forget the test_mydatabase may be not be the same
