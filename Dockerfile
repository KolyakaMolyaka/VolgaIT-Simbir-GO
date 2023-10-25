# pull official base image
FROM python:3.10-slim-buster

WORKDIR /usr/src/app
# set invironment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update 
RUN apt-get install -y netcat

# copy project
COPY . . 
# fix bug with restx 
RUN python ./flask_restx_script.py
RUN chmod +x ./entrypoint.sh 

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]