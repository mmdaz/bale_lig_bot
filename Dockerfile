FROM python:3.5
WORKDIR /LigBot
COPY ./ /LigBot
RUN pip install -r requirements.txt