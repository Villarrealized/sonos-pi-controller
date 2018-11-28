FROM villarrealized/debian-pygame-base
RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
COPY . /usr/src/app

CMD [ "python", "main.py"]
