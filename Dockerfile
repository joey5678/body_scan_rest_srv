FROM python:3.9-slim-buster

WORKDIR /app

# uwsgi must be compiled - install necessary build tools, compile uwsgi
# and then remove the build tools to minimize image size
# (buildDeps are removed, deps are kept)

# install other py libs - not require compilation
COPY requirements.txt /app/requirements.txt
#RUN pip install -r /app/requirements.txt

# copy source files
COPY conf /app/conf
COPY py /app/py
COPY migrations /app/migrations
COPY migrations_sqlite /app/migrations_sqlite
COPY scripts /app/scripts
COPY templates /app/templates
COPY test /app/test
COPY conf/loginscript.sh /etc/profile

# background spooler dir
RUN mkdir /tmp/pysrv_spooler

# we don't need this file with Docker but uwsgi looks for it
RUN echo `date +%s` >/app/VERSION

EXPOSE 80


# our server config file
# - you should write your own config file and put OUTSIDE the repository
#   since the config file contains secrets
# - here I use the sample template from repo
# - it is also possible to override the config with env variables, either here
#   or in Amazon ECS or Kubernetes configuration
COPY conf/server-config.json /app/real-server-config.json
# ENV PYSRV_DATABASE_HOST host.docker.internal
# ENV PYSRV_REDIS_HOST host.docker.internal
# ENV PYSRV_DATABASE_PASSWORD x

# build either a production or dev image
ARG BUILDMODE=production
ENV ENVBUILDMODE=$BUILDMODE

RUN echo "BUILDMODE $ENVBUILDMODE"

# run in shell mode with ENV expansion
#CMD uwsgi --ini /app/conf/uwsgi.ini:uwsgi-$ENVBUILDMODE
CMD bash
