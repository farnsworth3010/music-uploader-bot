FROM python:latest
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN apt update
RUN apt install -y exiftool
CMD ["python", "main.py"]
