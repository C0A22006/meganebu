FROM ubuntu:latest

RUN apt -y update
RUN apt -y upgrade

RUN apt install -y \
    autoconf \
    cmake \
    git \
    libtool libncurses5-dev libncursesw5-dev libtinfo5 \
    libffi-dev libssl-dev \
    openjdk-8-jdk \
    pkg-config \
    python3-pip \
    unzip \
    zip \
    zlib1g-dev

WORKDIR /home/lib
COPY requirements.txt requirements.txt

RUN pip install -U pip
RUN pip install cython
RUN pip install -r requirements.txt
RUN apt-get -y install tesseract-ocr tesseract-ocr-jpn
