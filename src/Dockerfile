FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /django
RUN apt-get update
RUN apt install -y libgl1-mesa-glx
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt