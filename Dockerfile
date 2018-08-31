FROM ubuntu
MAINTAINER Alex Serdiuk <serdy@yandex.ru>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    python-pip && mkdir /srv/dashboard
RUN pip install flask docker-py uwsgi boto3 GitHub-Flask Flask-SQLAlchemy

COPY ./templates /srv/dashboard/templates
COPY ./static /srv/dashboard/static
COPY ./*.py /srv/dashboard/
WORKDIR /srv/dashboard
CMD [ "uwsgi", "--http", "0.0.0.0:8080", "--enable-threads", "-p 2","-w", "start:app" ] 

