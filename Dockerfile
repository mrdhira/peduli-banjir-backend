FROM python:3.9

ARG ENV
ARG WORKER
ARG THREAD

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg2 dependencies
    libpq-dev

# copy source and install dependencies
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements/base.txt
RUN pip install -r requirements/${ENV}.txt
RUN chown -R www-data:www-data /app

CMD ["make", "start", "WORKER=2", "THREAD=2"]