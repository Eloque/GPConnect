# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /opt/app/
WORKDIR /opt/app
RUN pip install -r requirements.txt

COPY API .

EXPOSE 7500
