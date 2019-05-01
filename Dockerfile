FROM python:alpine

EXPOSE 5000

WORKDIR /srv/www/

RUN apk update && apk add build-base git \
&& git clone https://github.com/Nerevarishe/vista_portal.git

WORKDIR /srv/www/vista_portal

RUN pip install --no-cache-dir -r requirements.txt \
&& apk del build-base git


ENV FLASK_APP vista_portal
RUN flask db upgrade

CMD gunicorn -w 4 -b 0.0.0.0:5000 vista_portal:app
