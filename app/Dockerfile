FROM python:3.5
MAINTAINER Ethan Harstad "ethanharstad@gmail.com"
EXPOSE 8000
WORKDIR /code
RUN apt-get update
RUN apt-get install -y binutils libproj-dev gdal-bin python3-gdal
ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
