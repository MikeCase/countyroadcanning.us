FROM python:3.8-slim

WORKDIR /app/
ADD requirements.txt /app/

RUN pip install -r requirements.txt

ADD . /app/

EXPOSE 5050

CMD ["hypercorn", "wsgi:website", "--bind", "0.0.0.0:5050", "--reload"]