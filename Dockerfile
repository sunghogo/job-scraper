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

# Update system
RUN apt-get update && apt-get upgrade -y
# This breaks the bind mount for some reason: Error calling wrapper: Message: unknown error: cannot find Chrome binary
# RUN apt-get update \
#     && apt-get upgrade -y \
#     && apt-get install -y wget unzip ca-certificates libnss3 libnss3-tools libnspr4 \
#     && rm -rf /var/lib/apt/lists/

# Install wget
RUN apt-get install -y wget

# Download and install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# # Set Chromium version
# ENV CHROMIUM_VERSION=1058929

# # Download and extract Chromium v108
# RUN wget -q "https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/${CHROMIUM_VERSION}/chrome-linux.zip" -O /tmp/chromium.zip \
#     && mkdir -p /opt/chromium \
#     && unzip /tmp/chromium.zip -d /opt/chromium \
#     && rm /tmp/chromium.zip

# # Set path to include Chromium
# ENV PATH="/opt/chromium/chrome-linux:${PATH}"

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
CMD /wait && pytest tests_searches.py
# CMD python test_uc.py