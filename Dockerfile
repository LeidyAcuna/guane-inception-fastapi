# pull python image
FROM python:3.8-alpine

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/inception/

# Install python dependencies
RUN apk update \
 && apk add --no-cache python3-dev libffi-dev gcc postgresql-dev gcc musl-dev
RUN pip install --upgrade pip
RUN pip install pipenv pytest
COPY Pipfile Pipfile.lock /usr/src/inception/
RUN pipenv install --system --dev


# copy app
COPY . /usr/src/app/ 
EXPOSE 8000