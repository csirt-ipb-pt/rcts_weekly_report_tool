FROM nginxinc/nginx-unprivileged:1-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf

USER root

RUN mkdir -p /vol/static
RUN chmod 755 /vol/static
COPY ./src/static /vol/static

RUN apk update && \
    apk add --no-cache openssl && \
    openssl req -x509 -nodes -days 365 \
    -subj  "/C=PT/ST=PT/O=RCTS/CN=RCTS_Weekly_Reports.com" \
     -newkey rsa:2048 -keyout /vol/nginx-selfsigned.key \
     -out /vol/nginx-selfsigned.crt

RUN openssl dhparam -out /vol/dhparams.pem 4096

RUN chown nginx:nginx /vol/nginx-selfsigned.key
RUN chown nginx:nginx /vol/nginx-selfsigned.crt
RUN chown nginx:nginx /vol/dhparams.pem

USER nginx