FROM python:3.7-slim
WORKDIR /rul_pipeline
COPY requirements.txt /rul_pipeline
RUN pip install -r requirements.txt
COPY extract_data_rul.py /rul_pipeline