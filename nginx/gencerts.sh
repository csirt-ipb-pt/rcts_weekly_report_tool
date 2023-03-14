openssl req -newkey rsa:4096 -nodes -subj "/C=PT/ST=PT/O=RCTS/CN=RCTS_Weekly_Reports.com" -keyout ./privkey.pem -x509 -days 3650 -out ./fullchain.pem
openssl dhparam -out ./dhparams.pem 4096