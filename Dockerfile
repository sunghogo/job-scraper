FROM python:3.9

RUN apt-get update 

#download and install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

ENV HOME /root
WORKDIR /root

COPY . .

RUN pip3 install -r requirements.txt

# Expose container port 8000 for local access
EXPOSE 8000

CMD python scraper.py

# Commands to build / run the docker image
# docker build -t job-scraper .
# docker run -p 8080:8000 job-scraper