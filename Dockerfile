FROM python:3.6

RUN mkdir -p /usr/src/app
RUN mkdir /usr/src/app/uploads
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

# RUN pip install --no-cache-dir -r requirements.txt
# using aliyun mirror
RUN pip install --no-cache-dir -r requirements.txt --index-url=http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com

COPY . /usr/src/app

ENV FLASK_APP server.py

EXPOSE 5000
CMD [ "flask", "run", "--host", "0.0.0.0" ]
