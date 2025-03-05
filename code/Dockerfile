# Use Debian-based miniconda image
FROM continuumio/miniconda3:latest

RUN conda install python=3.11 -y && \
    apt-get update && apt-get install -y openjdk-11-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

RUN conda install -y pyspark pytorch numpy pandas scipy scikit-learn && \
    pip install \
    accelerate \
    awswrangler \
    datasets \
    duckdb \
    gensim \
    numba \
    onnxruntime \
    orjson \
    pandas \
    polars \
    pyarrow \
    pytest \
    s3fs \
    scikit-learn \
    scipy \
    seqeval \
    smart-open \
    spacy \
    sqlalchemy \
    torch \
    transformers \
    umap-learn

WORKDIR /app

COPY . /app

RUN pip install -r code/requirements.txt

CMD ["bash", "/app/code/script/run.sh"]
