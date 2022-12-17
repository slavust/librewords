# syntax=docker/dockerfile:1
ARG TRANSLATION_PACKAGES_DIR=/argos-translate-packages/

FROM slavust/argos-translate as language_packages
COPY $ARGOS_PACKAGES_DIR $TRANSLATION_PACKAGES_DIR

FROM python:3.10-slim-bullseye

COPY --from=language_packages $TRANSLATION_PACKAGES_DIR $TRANSLATION_PACKAGES_DIR
ENV ARGOS_PACKAGES_DIR=$TRANSLATION_PACKAGES_DIR
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

CMD python3 telegram-bot.py
