# Command to build docker image
# docker build -t job-scraper .

# Command to run docker image for WINDOWS
# docker run -v ${PWD}\outputs:/app/outputs -p 8080:5000 job-scraper
# Command to run docker image for LINUX/MACOS
# docker run -v $(pwd)\outputs:/app/outputs -p 8080:5000 job-scraper

# Select Python distribtion
FROM python:3.9

# Update system
RUN apt-get update && apt-get upgrade -y

# Install wget
RUN apt-get install -y wget

# Download and install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Set home/working directory to app
ENV HOME /app
WORKDIR /app

# Copy over files
COPY . .

# Install python dependencies
RUN pip3 install -r requirements.txt

# Expose container port 5000 for local access
EXPOSE 5000

# Add docker-compose-wait dependency to wait for dockerized database
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.11.0/wait /wait
RUN chmod +x /wait

# Run app
CMD /wait && ["python", "-u", "app.py"]