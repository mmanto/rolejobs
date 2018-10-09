FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
ADD . /code/
RUN cp rolejobs/local_settings.py.docker rolejobs/local_settings.py  
