FROM ubuntu:18.04

SHELL ["/bin/bash", "-c"]

# System packages
RUN apt-get update && apt-get install -y curl

# Install miniconda to /miniconda
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash Miniconda-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

WORKDIR /home
RUN mkdir -p /home/mof_tda
WORKDIR /home/mof_tda

# Create mof_tda env
RUN conda create -n mof_tda python=3.6
ENV PATH="/opt/conda/envs/mof_tda/bin:$PATH"

# Install mof_tda
RUN source activate mof_tda

RUN apt-get update
RUN apt-get install -y libcgal-dev cmake gcc g++ git && \
    export CXX=/usr/bin/g++ && \
    export CC=/usr/bin/gcc

COPY . /home/mof_tda

# TODO: resolve diode install in setup.py
RUN pip install --verbose git+https://github.com/mrzv/diode.git && \
    python setup.py develop && \
    pip install nose && \
    pip install coverage && \
    pip install pylint

RUN chmod +x dockertest.sh
CMD ["./dockertest.sh"]
