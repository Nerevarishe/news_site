FROM python:3
WORKDIR /srv/www/news_site/
COPY . .
EXPOSE 8000
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=news_site
RUN flask db upgrade
CMD gunicorn -w 4 -b 0.0.0.0:8000 news_site:app
