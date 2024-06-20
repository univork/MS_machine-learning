FROM python:3.11 as base

FROM base as scraper-build
# installing google-chrome-stable 
RUN apt-get install -y gnupg wget curl unzip --no-install-recommends; \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | \
    gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/google.gpg --import; \
    chmod 644 /etc/apt/trusted.gpg.d/google.gpg; \
    echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list; \
    apt-get update -y; \
    apt-get install -y google-chrome-stable;

# installing chromedriver
RUN CHROMEDRIVER_VERSION=$(curl https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE); \
    wget -N https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip -P ~/ && \
    unzip ~/chromedriver-linux64.zip -d ~/ && \
    rm ~/chromedriver-linux64.zip && \
    mv -f ~/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    rm -rf ~/chromedriver-linux64

# set display port to avoid crash
ENV DISPLAY=:99

RUN pip install --upgrade pip

WORKDIR /scraper
COPY ./scraper/requirements.txt .
RUN pip install -r requirements.txt
COPY ./scraper .

CMD ["python", "scraper.py"]

FROM base as app-build

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /work
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt
COPY ./app ./app
COPY ./models ./models

CMD ["python", "-m", "app.app"]
