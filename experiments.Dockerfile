FROM python:3.6.3-slim
LABEL Name=habitat-experiments Version=0.0.1
WORKDIR /app
COPY ./notebooks /app
COPY ./requirements.txt /app
COPY ./data/current_measurements.json /app/current_measurements.json
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
EXPOSE 3333
CMD ["jupyter", "notebook", "--ip='*'", "--port=3333", "--no-browser", "--allow-root"]
