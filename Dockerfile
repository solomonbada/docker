FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y 
COPY . .
RUN pip3 install virtualenv
RUN virtualenv venv
RUN . /venv/bin/activate
RUN chmod 777 ./requirements.txt
RUN pip3 install -r ./requirements.txt 
ENTRYPOINT ["/usr/bin/python3", "run.py"]
