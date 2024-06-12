FROM quay.io/jupyter/minimal-notebook

WORKDIR /home/jovyan/work

COPY ./requirements.txt /home/jovyan/work

RUN pip install -r requirements.txt

COPY . /home/jovyan/work/
