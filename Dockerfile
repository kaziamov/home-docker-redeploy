FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN apt-get update \
	&& apt-get install -y docker.io \
	&& pip install flask
EXPOSE 5000
CMD ["python", "app.py"]
