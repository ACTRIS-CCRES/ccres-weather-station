
FROM python:3.10-bullseye

LABEL description="ccres_weather_station docker image"

RUN apt-get update \
    && apt-get install -y --no-install-recommends libudunits2-dev gdb \
    && rm -rf /var/lib/apt/lists/*


COPY . .

RUN pip install .[dev]

ENTRYPOINT [ "python" ]
