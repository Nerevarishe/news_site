FROM python:alpine

EXPOSE 5001

WORKDIR /srv/www/news_site/

COPY ./news_site .

RUN apk update && apk add build-base \
&& pip install --no-cache-dir -r requirements.txt \
&& apk del build-base

ENV FLASK_APP news_site
RUN flask db upgrade

CMD gunicorn -w 4 -b 0.0.0.0:5001 news_site:app
