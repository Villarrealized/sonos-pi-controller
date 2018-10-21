FROM bytegenesis/python3-build-base
RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt
COPY . /usr/src/app

CMD [ "python3", "main.py"]
