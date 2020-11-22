FROM python:3.8
COPY requirements.txt /
RUN pip install -r requirements.txt
WORKDIR /app

COPY app/ /app/
ENV FLASK_APP=app.py
CMD flask db upgrade && flask run -h 0.0.0.0 -p 5000