FROM ubuntu:16.10
RUN apt-get update && apt-get install -y nodejs npm imagemagick python-pip
RUN apt-get clean all
RUN ln /usr/bin/nodejs /usr/bin/node
RUN npm -g install phantomjs-prebuilt
RUN mkdir /code
ADD requirements.txt  /code
WORKDIR /code
RUN pip install -r requirements.txt
ADD .  /code
EXPOSE 5001
CMD ["python", "app.py"]
