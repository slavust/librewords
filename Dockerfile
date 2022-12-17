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
CMD python3 -c "import nltk; nltk.download('punkt')" && \
    python3 -c "import nltk; nltk.download('stopwords')" && \
    python3 -c "import nltk; nltk.download('wordnet')" && \
    python3 -c 'import argostranslate.package; import argostranslate.argospm; argostranslate.package.update_package_index(); argostranslate.argospm.install_all_packages()' && \
    python3 telegram-bot.py
