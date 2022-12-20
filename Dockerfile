# syntax=docker/dockerfile:1

FROM python:3.10-slim-bullseye
WORKDIR /bot
RUN apt-get update && apt-get install -y \
                                        build-essential \
                                        protobuf-compiler \
                                        libprotobuf-dev
COPY requirements.txt requirements.txt
COPY *.py ./
RUN pip3 install -r requirements.txt

RUN python3 -c "import nltk; nltk.download('punkt')" && \
    python3 -c "import nltk; nltk.download('stopwords')" && \
    python3 -c "import nltk; nltk.download('wordnet')"

RUN python3 -c "import argostranslate.package; argostranslate.package.update_package_index()" && \
    python3 -c "import argostranslate.argospm; argostranslate.argospm.install_all_packages()"

CMD python3 telegram-bot.py
