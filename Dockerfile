FROM python:3.7-alpine

RUN adduser -D workoutapi

WORKDIR /home/workoutapi

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY workout workout
COPY migrations migrations
COPY workoutapi.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP workoutapi.py

RUN chown -R workoutapi:workoutapi ./
USER workoutapi

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]