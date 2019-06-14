FROM continuumio/miniconda3

# Activate shell
SHELL ["/bin/bash", "-c"]

WORKDIR /home
RUN mkdir -p /home/mof_tda
WORKDIR /home/mof_tda

# Create mof_tda env
RUN conda create -n mof_tda python=3.6
ENV PATH="/opt/conda/envs/mof_tda/bin:$PATH"


# Install mof_tda
RUN source /opt/conda/bin/activate mof_tda

# Update mysql/postgres
RUN apt-get update
RUN apt-get install -y libcgal-dev cmake gcc

COPY . /home/mof_tda

# TODO: resolve diode install in setup.py
RUN pip install --verbose git+https://github.com/mrzv/diode.git && \
    python setup.py develop && \
    pip install nose && \
    pip install coverage && \
    pip install pylint

RUN chmod +x dockertest.sh
CMD ["./dockertest.sh"]
