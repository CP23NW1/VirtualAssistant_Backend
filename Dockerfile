FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get -y autoremove --purge openssl && apt-get install -y build-essential libssl-dev ca-certificates libasound2 wget 

RUN apt-get install -y  pulseaudio alsa-base alsa-utils sox libsox-fmt-all 

ENV PULSE_SERVER=host.docker.internal

RUN wget -O - https://www.openssl.org/source/openssl-1.1.1w.tar.gz | tar zxf - 
RUN cd openssl-1.1.1w \
    ./config --prefix=/usr/local \
    make -j $(nproc) \
    make install_sw install_ssldirs 
RUN ldconfig -v 
ENV SSL_CERT_DIR=/etc/ssl/certs
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

WORKDIR /app

RUN apt-get install -y python3-pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN pip install uvicorn
RUN pip install --upgrade azure-cognitiveservices-speech

CMD ["uvicorn", "app.main:app", "--reload" ,  "--host=0.0.0.0", "--port=8000"]


