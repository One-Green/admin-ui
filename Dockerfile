ARG ARG_PYARROW_CMAKE_OPTIONS

FROM python:3.8.5

ENV PYTHONUNBUFFERED TRUE
ENV PYARROW_CMAKE_OPTIONS $ARG_PYARROW_CMAKE_OPTIONS

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip

RUN apt update && apt install -y ca-certificates lsb-release wget cmake \
    && wget https://apache.bintray.com/arrow/$(lsb_release --id --short | tr 'A-Z' 'a-z')/apache-arrow-archive-keyring-latest-$(lsb_release --codename --short).deb \
    && apt install -y ./apache-arrow-archive-keyring-latest-$(lsb_release --codename --short).deb \
    && apt update \
    && apt install libarrow-dev  libarrow-python-dev -y \
    && pip install pyarrow

RUN pip install -r requirements.txt

ENTRYPOINT []
