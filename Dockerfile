FROM python:3.7-slim

ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /code
COPY ./ /code
RUN pip install -r requirement.txt
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=1", "--thread=1", "main:app"]