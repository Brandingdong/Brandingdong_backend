FROM        python:3.8-slim

RUN         apt-get -y -qq update && \
            apt-get -y -qq dist-upgrade && \
            apt-get -u -qq autoremove

RUN         apt -y install nginx

# requirements.txt 복사
COPY        ./requirements_base.txt /tmp/
COPY        ./requirements.txt /tmp/
RUN         pip install -r /tmp/requirements.txt

# 소스코드 복사
COPY        . /srv/brandingdong
WORKDIR     /srv/brandingdong/apps

# Nginx 기본 설정 삭제 & 설정 파일 복사
RUN         rm /etc/nginx/sites-enabled/default
RUN         cp /srv/brandingdong/.config/production/brandingdong.nginx /etc/nginx/sites-enabled/

RUN         mkdir /var/log/gunicorn

CMD         /bin/bash