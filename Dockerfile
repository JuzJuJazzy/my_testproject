FROM python:3.11-buster
WORKDIR /srv/flask_app

ENV FLASK_ENV=production

RUN chown -R www-data:www-data /srv/flask_app
RUN apt update && apt upgrade -y
RUN apt install -y nginx python3-dev libmariadb3 build-essential libffi-dev python-openpyxl python3-openpyxl

COPY --chown=www-data:www-data . /srv/flask_app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi

COPY .containers/nginx/nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]
