# pull official base image
FROM debian:10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

# install psycopg2 dependencies
RUN apt update
RUN apt install gcc python3-dev musl-dev python3-pip cron -y


RUN python3 -m pip install --upgrade pip
COPY . /code/

RUN python3 -m pip install -r requirements.txt


EXPOSE 8000

RUN ["chmod", "+x", "./entrypoint.sh"]

CMD ["./entrypoint.sh"]