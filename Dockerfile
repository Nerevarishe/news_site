FROM python:3
WORKDIR /src/news_site/
COPY . .
EXPOSE 8000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD gunicorn -w 4 -b 0.0.0.0:8000 app:app