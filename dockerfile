FROM continuumio/miniconda3:latest

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/legitShivam/system-resource-monitor.git .

RUN conda env create -f environment.yml
RUN echo "source activate system-resource-monitor" >> ~/.bashrc
ENV PATH /opt/conda/envs/system-resource-monitor/bin:$PATH

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "src/__main__.py", "--server.port=8501", "--server.address=0.0.0.0"]
