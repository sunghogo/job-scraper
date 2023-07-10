# Command to build docker image
# docker build -t job-scraper .
# Command to run docker image for WINDOWS
# docker run -v ${PWD}\outputs:/root/outputs -p 8080:8000 job-scraper
# Command to run docker image for LINUX/MACOS
# docker run -v $(pwd)\outputs:/root/outputs -p 8080:8000 job-scraper

# Select Python distribtion
FROM python:3.9

# Update system
RUN apt-get update && apt-get upgrade -y

# Install wget
RUN apt-get install -y wget

# Download and install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Set home/working directory
ENV HOME /root
WORKDIR /root

# Copy over files
COPY . .

# Install python dependencies
RUN pip3 install -r requirements.txt

# Expose container port 8000 for local access
EXPOSE 8000

# Run app
CMD ["python", "-u", "scraper/scraper.py"]