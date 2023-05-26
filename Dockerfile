FROM python:3.8-slim-buster

# UPDATE
RUN pip install --upgrade pip
RUN apt-get update -y && apt-get upgrade -y

# INSTALL requirements
WORKDIR /

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# APP
COPY src /app
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["/app/main.py"]