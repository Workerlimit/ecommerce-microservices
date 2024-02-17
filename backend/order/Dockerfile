FROM python:3.9.2-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY module.py .
COPY app.py .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]