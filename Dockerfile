# pull python image
FROM python:3.8.1-alpine

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/inception/

# Install python dependencies
RUN apk update \
 && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install pipenv pytest
COPY Pipfile Pipfile.lock /usr/src/inception/
RUN pipenv install --system --dev

# copy app
COPY . /usr/src/app/ 
EXPOSE 8000