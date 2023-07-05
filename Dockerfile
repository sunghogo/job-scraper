FROM python:3.9

# Update system
RUN apt-get update && apt-get upgrade -y

# Install wget
RUN apt-get install -y wget

# # Add Google Chrome to the sources list
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list

# # update the system with new sources list
# RUN apt-get update -y

# # Install Google Chrome
# RUN apt-get install -y google-chrome-stable

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
# docker run -v ${PWD}\outputs:/root/outputs -p 8080:8000 job-scraper