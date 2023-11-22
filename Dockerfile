FROM python:3.10.10-slim

WORKDIR /app

RUN apt-get install -y python3-pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN pip install uvicorn
RUN pip install --upgrade azure-cognitiveservices-speech
RUN pip install pydantic[email]
RUN pip install fastapi-jwt-auth[asymmetric]

EXPOSE 7000

CMD ["uvicorn", "app.main:app"]


