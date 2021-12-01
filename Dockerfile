
FROM python:3.9.9

WORKDIR /app

RUN pip install --upgrade pip
RUN pip3 install pyyaml aiohttp 

COPY . .

EXPOSE 8080

CMD [ "python", "./vitality_server_aio.py"]
