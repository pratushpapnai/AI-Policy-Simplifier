FROM python:3.11-slim

ENV PYTHONPATH=/code

WORKDIR /code

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY . .
RUN chmod +x start.sh
EXPOSE 7860

CMD ["./start.sh"]  