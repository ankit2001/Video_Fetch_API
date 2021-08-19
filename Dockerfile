FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt
RUN pip3 install --upgrade google-api-python-client
RUN pip3 install -U drf-yasg

RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./ /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user