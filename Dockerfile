
FROM python:3.6.8

WORKDIR /app

RUN pip install --upgrade pip
RUN pip3 install requests-pkcs12 

COPY . .

CMD [ "python", "./vitality_server.py"]
