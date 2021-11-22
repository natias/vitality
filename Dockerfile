
FROM python:3.9.9

WORKDIR /app

RUN pip install --upgrade pip
RUN pip3 install pyyaml aiohttp requests-toolbelt cryptography pyOpenSSL

COPY . .

CMD [ "python", "./vitality_server.py"]
