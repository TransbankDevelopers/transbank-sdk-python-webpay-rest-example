FROM tiangolo/uwsgi-nginx-flask:python3.7-alpine3.7
RUN apk --update add bash nano
RUN  pip install --upgrade pip
