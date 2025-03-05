# Use Debian-based miniconda image
FROM continuumio/miniconda3:latest

RUN conda install python=3.11 -y

RUN conda install -y pyspark pytorch numpy pandas scipy scikit-learn && \
    pip install polars orjson pyarrow awswrangler transformers accelerate duckdb s3fs umap-learn smart-open onnxruntime spacy seqeval gensim numba sqlalchemy pytest datasets

WORKDIR /app

COPY . /app
COPY config/config.yaml /app/config/config.yaml

RUN pip install -r code/requirements.txt

CMD ["bash", "/app/code/script/run.sh"]
