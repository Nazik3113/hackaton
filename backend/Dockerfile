FROM python:3.9

WORKDIR /code

COPY . .

RUN pip install fastapi
RUN pip install pydantic
RUN pip install requests
RUN pip install uvicorn

CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8000"]