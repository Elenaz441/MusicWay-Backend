FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN git clone https://github.com/aubio/aubio.git && \
    cd aubio && \
    python setup.py build_ext --inplace && \
    python setup.py install && \
    cd ..

RUN apt-get update && apt-get install -y ffmpeg netcat-openbsd

COPY ./src /code/src

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]