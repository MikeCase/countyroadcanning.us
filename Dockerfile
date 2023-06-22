FROM python:3.8-slim

WORKDIR /app/
ADD requirements.txt /app/

RUN pip install -r requirements.txt

ADD . /app/

EXPOSE 5000

CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:5000", "--reload"]