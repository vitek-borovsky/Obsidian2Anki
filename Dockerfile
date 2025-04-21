FROM python:latest

RUN groupadd -g 1001 anki && \
    useradd -u 1001 -g anki -m anki

WORKDIR /home/anki/
RUN mkdir src

COPY src/requirements.txt src/requirements.txt

RUN pip install -r src/requirements.txt

COPY src src

VOLUME [ "/home/anki/.ssh" ]

# ENTRYPOINT [ "/home/anki/main.py" ]
