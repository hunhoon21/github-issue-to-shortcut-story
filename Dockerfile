FROM python:3.8-slim-buster

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

RUN pip install requests

COPY src/main.py main.py
CMD ["python", "/app/main.py"]