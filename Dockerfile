FROM python:3.9.15-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /opt/drf-class-rotator

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY drg_class_rotator .

CMD ["python", "main.py"]