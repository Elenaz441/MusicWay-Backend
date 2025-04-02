FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN git clone https://github.com/aubio/aubio.git && \
    cd aubio && \
    python setup.py build_ext --inplace && \
    python setup.py install && \
    cd ..

RUN apt-get update && apt-get install -y ffmpeg

COPY ./src /code/src

CMD ["alembic", "upgrade", "head"]
CMD ["fastapi", "run", "src/main.py", "--port", "8000"]