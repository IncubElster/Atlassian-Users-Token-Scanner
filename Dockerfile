FROM python:3.12-alpine
WORKDIR /
COPY . .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
ENTRYPOINT []