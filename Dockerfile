FROM python:3


ADD analizing_server.py /

COPY . /Parsix_APP 

CMD ["python3", "./analizing_server.py"]


