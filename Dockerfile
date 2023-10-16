FROM python:3.9

ENV POETRY_VENV=/app/.venv

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt-get -qq install --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade "jax[cuda11_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
RUN pip install --upgrade clu
RUN git clone https://github.com/google/flax.git
RUN pip install --user -e flax

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools tensorflow torch torchvision \
    && $POETRY_VENV/bin/pip install poetry==1.6.1

ENV PATH="${PATH}:${POETRY_VENV}/bin"

RUN git clone https://github.com/ggerganov/whisper.cpp.git
RUN cd whisper.cpp && make && ./main -f samples/jfk.wav

WORKDIR /app

COPY . ./

RUN poetry config virtualenvs.in-project true
RUN poetry install
RUN pip install cached_property ffmpeg
RUN pip install -e .["endpoint"]

EXPOSE 8081

CMD ["uvicorn", "webservice.webservice:app", "--host", "0.0.0.0", "--port", "8081"]
