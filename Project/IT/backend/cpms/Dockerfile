# pull official base image
FROM python:3.10.6

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nano \
    zip \
    unzip \
    vim \
    gdal-bin  \
    libgdal-dev \
    python3-gdal \
    binutils  \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Change the current working directory
WORKDIR /usr/src/emsp

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG ENVIRONMENT

# Install required packages from environment specific requirements file
COPY requirements ./requirements
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements/${ENVIRONMENT}.txt

# Copy the project
COPY . .
