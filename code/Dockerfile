# Use Debian-based miniconda image
FROM continuumio/miniconda3:latest

# Install a specific Python version (using a modern version, Python 3.11)
RUN conda install python=3.11 -y

# Install required packages via conda and pip
RUN conda install -y pyspark pytorch numpy pandas scipy scikit-learn && \
    pip install polars orjson pyarrow awswrangler transformers accelerate duckdb s3fs umap-learn smart-open onnxruntime spacy seqeval gensim numba sqlalchemy pytest datasets

# Set the working directory
WORKDIR /app

# Copy the project files into the Docker image
COPY . /app

# Install additional requirements from requirements.txt
RUN pip install -r code/requirements.txt

# Command to run the application using the provided bash script
CMD ["bash", "/app/code/script/run.sh"]
