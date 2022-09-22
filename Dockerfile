FROM python:3.8-alpine

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk add --update curl gcc g++ zip
RUN pip3 install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /src
COPY ./src /src
WORKDIR /src
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN adduser -D user
RUN chown -R user:user /src
RUN chmod -R 755 /src/upload
RUN python3 manage.py makemigrations && python3 manage.py migrate 
USER user

CMD ["entrypoint.sh"]