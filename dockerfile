FROM python.3.11.0-alpine3.16 

RUN pip install --upgrade pip

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

RUN ./manage.py migrate

EXPOSE 8080

CMD ["python3", "manage.py", "runserver"]

