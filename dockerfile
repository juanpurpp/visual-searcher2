FROM python:3.9

WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./main.py /code/

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]