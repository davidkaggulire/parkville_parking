FROM python:3.8-slim

# -- to install python package psycopg2 (for postgres) -- #
# RUN apt-get update
# RUN apt-get install -y postgresql libpq-dev postgresql-client postgresql-client-common gcc

# add user (change to whatever you want)
# prevents running sudo commands
# RUN useradd -r -s /bin/bash dkaggs

# set current env
ENV HOME /app
WORKDIR /app
ENV VIRTUAL_ENV=/opt/venv


# RUN chown -R alex:alex /app
# USER alex

# set app config option
ENV FLASK_ENV=testing

# set argument vars in docker-run command
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
# -- AWS RDS vars -- #
ARG POSTGRES_USER
ARG POSTGRES_PW
ARG POSTGRES_URL
ARG POSTGRES_DB

ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DATABASE_URL
ARG SECRET_KEY

ENV DB_NAME $DB_NAME
ENV DB_USER $DB_USER
ENV DB_PASSWORD $DB_PASSWORD
ENV DATABASE_URL $DATABASE_URL
ENV SECRET_KEY $SECRET_KEY


ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION

# create virtualenv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/app/.local/bin:${PATH}"


# Avoid cache purge by adding requirements first
ADD ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

# Add the rest of the files
COPY . /app
WORKDIR /app

# start web server
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "api:app", "--workers=5"]

CMD ["gunicorn", "-b", "127.0.0.1:5000", "run:app", "--workers=5"]