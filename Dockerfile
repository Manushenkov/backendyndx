FROM python:3.8

RUN pip3 install --upgrade pipenv

WORKDIR /app
COPY . /app

RUN pipenv install

EXPOSE 80

ENTRYPOINT [ "pipenv" ]
CMD ["run", "flask","run" , "--port=80", "--host=0.0.0.0"]