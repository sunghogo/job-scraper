# Command to build docker image
# docker build -t job-scraper .

# Command to run docker image for WINDOWS
# docker run -v ${PWD}\outputs:/app/outputs -p 8080:5000 job-scraper
# Command to run docker image for LINUX/MACOS
# docker run -v $(pwd)\outputs:/app/outputs -p 8080:5000 job-scraper

# Win 10 Docker Issue where it does not automatically release space: Docker -> Troubleshoot -> Clean / Purge Data
# https://github.com/docker/for-win/issues/244

# Select Python distribtion
FROM python:3.9

# Update system and install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y wget unzip ca-certificates libnss3 libnss3-tools libnspr4

# Download and install older version of chrome (v104) from slimjet
ENV DEB_PACKAGE="google-chrome-stable_current_amd64.deb"

RUN wget -q "https://www.slimjet.com/chrome/download-chrome.php?file=files%2F104.0.5112.102%2F${DEB_PACKAGE}" -O "/tmp/${DEB_PACKAGE}" && \
    dpkg -i "/tmp/${DEB_PACKAGE}" || true && \
    apt-get install -f -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm "/tmp/${DEB_PACKAGE}"

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
# CMD /wait && pytest tests_searches.py
CMD python test_uc.py