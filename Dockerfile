FROM python:3.9

ENV PYTHONNUMBUFFERED 1
WORKDIR /app 

COPY ../../MPM_ORD/backend/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt 

COPY . /app 

CMD python main.py
