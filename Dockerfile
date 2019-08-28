FROM ubuntu:18.04

SHELL ["/bin/bash", "-c"]

# System packages, Miniconda
RUN apt-get update && apt-get install -y curl && \
    curl -LO http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b && \
    rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

WORKDIR /home
RUN mkdir -p /home/mof_tda
WORKDIR /home/mof_tda

RUN apt-get update && \
    apt-get install -y libcgal-dev cmake gcc g++ git && \
    export CXX=/usr/bin/g++ && \
    export CC=/usr/bin/gcc && \
    # install mongodb
    apt-get install -y mongodb


COPY . /home/mof_tda

# TODO: resolve diode install in setup.py
RUN python setup.py develop && \
    pip install nose && \
    pip install coverage && \
    pip install pylint

RUN chmod +x dockertest.sh
CMD ["./dockertest.sh"]
