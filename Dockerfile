
FROM python:3.10-bullseye

LABEL description="ccres_weather_station docker image"

RUN apt-get update \
    && apt-get install -y --no-install-recommends libudunits2-dev gdb \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY . /ccres_weather_station/

RUN pip install /ccres_weather_station[dev]
