FROM python:3.8-slim-buster

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

COPY requirements.txt /tmp/pip-tmp/
RUN pip install -U pip &&\
    pip install --no-cache-dir -r /tmp/pip-tmp/requirements.txt &&\
    rm -rf /tmp/pip-tmp

ARG NOTION_TOKEN
ARG NOTION_DATABASE_ID
ENV NOTION_TOKEN=${NOTION_TOKEN}
ENV NOTION_DATABASE_ID=${NOTION_DATABASE_ID}

COPY src/ /etc/mysrc/
WORKDIR /etc/mysrc/
