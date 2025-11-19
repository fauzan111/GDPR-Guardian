# 1. Base Image
FROM python:3.9-slim

# 2. Set work directory
WORKDIR /code

# 3. Install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 4. Download NLP Models (Baking them into the image)
RUN python -m spacy download it_core_news_lg
RUN python -m spacy download en_core_web_lg

# 5. Copy Code
COPY ./app /code/app

# 6. Run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]