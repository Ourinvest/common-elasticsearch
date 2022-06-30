# Pull base image
FROM python:3.8

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y -q
RUN apt-get install -y -q git

RUN pip install poetry

# Configuring poetry
RUN poetry config virtualenvs.create false

WORKDIR /code
COPY . /code

RUN poetry export -f requirements.txt --without-hashes > requirements-poetry.txt
RUN pip install -r requirements-poetry.txt
RUN pip install -r requirements.txt

RUN apt update
RUN apt install nodejs -y
RUN apt install npm -y
RUN npm config set strict-ssl=false
RUN npm install -g dynalite

CMD ["python3","-m","system"]
