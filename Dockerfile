FROM alpine:3.6

# Change working directory
WORKDIR /usr/src/app

# ENV
ENV LANG=en_US.UTF-8 \
    LC_ALL=C.UTF-8 \
    PIPENV_HIDE_EMOJIS=1

# Install packages
RUN apk add --no-cache bash
RUN apk add --no-cache \
  python3 \
  python3-dev \
  linux-headers \
  gcc \
  musl-dev \
  libffi-dev \
  postgresql-dev \
  libstdc++

RUN apk add --no-cache --virtual .build-deps g++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

# Copy docker-entrypoint.sh
COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Update all packages
RUN apk upgrade --no-cache

# Update pip and setuptools
RUN pip3 install --upgrade --no-cache-dir pip setuptools uwsgi pipenv
RUN ln -sf /usr/local/bin/python /bin/python

ENV PYTHONPATH=pipenv

# Copy Djnago project to working directory
COPY . .

# pipenv install project packages
RUN pipenv --three --site-packages
RUN pipenv lock --requirements > requirements.txt
RUN pip3 install -r requirements.txt

RUN apk del .build-deps

# Volumes
VOLUME /usr/src/app/log
VOLUME /usr/src/app/media
VOLUME /usr/src/app/assets
VOLUME /usr/src/app/static

# Posts
EXPOSE 8080

# Run!
ENTRYPOINT [ "docker-entrypoint.sh" ]
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]