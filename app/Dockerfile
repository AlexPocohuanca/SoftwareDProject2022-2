FROM python:latest
COPY . /app
WORKDIR /app
EXPOSE 5000
EXPOSE 3306
EXPOSE 3308
RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
CMD python3 app.py
