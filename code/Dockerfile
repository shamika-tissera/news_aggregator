# Use Debian-based miniconda image
FROM continuumio/miniconda3:latest

RUN conda install python=3.11 -y

RUN apt-get update && apt-get install -y openjdk-11-jdk

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

RUN conda install -y pyspark pytorch numpy pandas scipy scikit-learn && \
    pip install polars orjson pyarrow awswrangler transformers accelerate duckdb s3fs umap-learn smart-open onnxruntime spacy seqeval gensim numba sqlalchemy pytest datasets

WORKDIR /app

COPY . /app

RUN pip install -r code/requirements.txt

CMD ["bash", "/app/code/script/run.sh"]
