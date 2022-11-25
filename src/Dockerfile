FROM python:3.10.8-slim-buster
COPY . /root/postgres_air
WORKDIR /root/postgres_air
RUN python3 -m pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "postgres_air.app:app", "--host", "0.0.0.0", "--port", "8000"]