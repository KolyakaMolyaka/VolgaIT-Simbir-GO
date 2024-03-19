FROM python:3.11-slim-buster
RUN apt-get update
RUN pip install --upgrade pip