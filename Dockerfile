FROM python:3.6
ADD . /app
WORKDIR /app
RUN pip install -r ./requirements.txt

CMD gunicorn --bind 0.0.0.0:$PORT pkg.web.app:app