FROM python:3.8
ENV PYTHONUNBUFFERED=1
ENV PATH="/scripts:${PATH}"
RUN apt-get update
RUN apt install -y libgl1-mesa-glx
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir /app
ADD . /app
WORKDIR /app

COPY ./scripts /scripts
RUN chmod +x /scripts/*

RUN mkdir -p /web/media_cdn
RUN mkdir -p /web/static_cdn

RUN chown -R root:root /web
RUN chmod -R 755 /web


CMD ["entrypoint.sh"]