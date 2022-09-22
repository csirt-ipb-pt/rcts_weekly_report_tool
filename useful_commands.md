# Useful Commands

The following documentation has useful commands for Django and for building Docker images.

## Django

### Install django

```
pip3 install django==3.1.2
```

### Create project

```
mkdir src
cd src
django-admin startproject "name" .
```

### Run server

```
python3 manage.py runserver
```

### Sinc Settings

```
python3 manage.py makemigrations
python3 manage.py migrate
```

### Create Super User

```
python3 manage.py createsuperuser
```

### Creta APP

```
python3 manage.py startapp "name"
```

### Reset Database

+ This command will reset the database, and remove users.

```
python3 manage.py flush
```

### Change static files directory

+ After changing the static files directory run the following command.

```
python3 manage.py collectstatic --noinput
```

## Docker Build

+ After creating the Dockerfile, run the following command to give a name and version to the image about to be created.

```
sudo docker build . -t "name":"version"
```