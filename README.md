# RCTS Weekly Report Tool

RCTS Weekly Report Tool is a Python Django based tool that helps keep all the records from the Weekly Reports sent by PT RCTS CERT, stored on a DB and automates the process of analyzing them.

![](RCTS_Weekly_Report_Tool.gif)

The following links contain a document with useful commands related to Django, and a python script that generates random strings of characters that can be used as the secret key of the tool.

- [Useful Commands](./useful_commands.md) for Django and Docker.

- [Secret_Key](./secret_key.py) is a python script that generates a random string of 50 characters, with uppercase, lowercase, digits and special characters.

## Default Credentials

```
User: admin
Password: randompassword123
```

## Useful Information

The following commands need to be executed inside the container, on directory `src`.

To reset the database, and remove users, run the following command.

```
python3 manage.py flush
```

To create a new superuser.

```
python3 manage.py createsuperuser
```

To change the default password, either reset the database and create a new superuser, or go to the admin webpage.

```
http://weekly-reports_ip:8080/admin/
```

## Network Infrastructure

Before building the containers, make sure to edit the following file:

+ ./src/network_infrastructure.py

The file needs variables `network_names` and `network_range` to be filled with information from the Network Infrastructure for the tool to work.

`network_names` is a list that contains the names of the networks.

`network_range` is a dictionary. The keys are the names of the Networks, and its values are the First valid IP from the Network, and the Last valid IP from the same Network.

An example can be seen below:

```
network_names = ('Network1', 'Network2')

network_range = dict([('Network1', ('10.1.1.0', '10.1.1.255')), ('Network2', ('10.1.2.0', '10.1.2.255'))])
```

## Creating the Container

To build the docker container, execute the following command.

```
docker-compose build
```

## Start/Stop the RCTS Weekly Report Tool

To start the container, execute the following command.

```
docker-compose up -d
```

To stop it, execute the following command.

```
docker-compose down
```

## Variables

These variables can be found on the [docker-compose.yaml](./docker-compose.yml) file.

+ DEBUG

    ```
    - DEBUG=0
    ```

    + By default 0, if set to 1, Django Debugger will be set true and only the host machine will have access to the web interface to test it.

+ SECRET_KEY

    ```
    - SECRET_KEY=samplesecretkey123
    ```

    + The Secret Key of Django, replace it with a strong and unique, unpredictable string. The default values is a random string of 50 characters generated every time Django is started.

+ ALLOWED_HOSTS

    ```
    - ALLOWED_HOSTS=*
    ```

    + The allowed hosts to access Django, "*" to allow everyone, or specify by IP which host will have access.

+ PASSWORD

    ```
    - PASSWORD=randompassword123
    ```

    + Password that encrypts the zip file with the fields extracted from each table of the Database.

## Nginx Reverse Proxy Config

If you intend to use a different Nginx than the one provided, make sure to copy the `static` folder from inside the `src` directory into the Nginx server, and add the following lines to the config file.

```
server {
    location /static/ {
        alias /path/to/static/folder/;
    }

    location / {
        proxy_pass http://weekly-reports_ip:8000;
    }
}
```

## API

The API is implemented to the Other, Malware and Vulnerabilities tables, being able to `GET` entries by their IP, `POST` new entries or `PUT` to update an existing entry.

Below is an example on how to invoke the API.

+ GET

    ```
    curl --insecure -u user:password -X GET https://IP:PORT/api/table/?ip=192.168.1.3
    ```

+ POST

    Depending on the table, the parameters can be different from one another.

    + other and mal table

    ```
    curl --insecure -u user:password -X POST https://IP:PORT/api/table/ -H 'Content-Type: application/json' -d '{"ip": "192.168.1.3", "rede": "Network", "data_1": "2022-05-02T20:07:23+00:00", "data_2": "2022-05-02T20:07:23+00:00", "count": "10"}'
    ```

    + vul table

    ```
    curl --insecure -u user:password -X POST https://IP:PORT/api/vul/ -H 'Content-Type: application/json' -d '{"ip": "192.168.1.3", "port": "11111", "rede": "Network", "data_1": "2022-05-02T20:07:23+00:00", "data_2": "2022-05-02T20:07:23+00:00", "count": "10"}'
    ```

+ PUT

    Depending on the table, the parameters can be different from one another.

    + other and mal table

    ```
    curl --insecure -u user:password -X PUT https://IP:PORT/api/table/?ip=192.168.1.3  -H 'Content-Type: application/json' -d '{"rede": "ESA", "data_1": "2022-05-02T20:07:23+00:00", "data_2": "2022-05-02T20:07:23+00:00", "count": "20"}'
    ```

    + vul table

    ```
    curl --insecure -u user:password -X POST https://IP:PORT/api/vul/?ip=192.168.1.3 -H 'Content-Type: application/json' -d '{"port": "11112", "rede": "Network", "data_1": "2022-05-02T20:07:23+00:00", "data_2": "2022-05-02T20:07:23+00:00", "count": "20"}'
    ```