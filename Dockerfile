# 1. Base Image
FROM python:3.9-slim
WORKDIR /code

# dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


RUN python -m spacy download it_core_news_lg
RUN python -m spacy download en_core_web_lg

#  Code
COPY ./app /code/app

# API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
