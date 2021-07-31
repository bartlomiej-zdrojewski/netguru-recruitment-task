FROM python:3.9
WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY ./src /app/

CMD ["./wait-for-it.sh", "db:5432", "-t", "30", "--", "./init.sh"]
