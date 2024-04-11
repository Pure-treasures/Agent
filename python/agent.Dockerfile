ARG PYTHON_VERSION=3.9
ARG BASE_IMAGE=python:${PYTHON_VERSION}-slim
ARG VENV_PATH=/prod_venv

FROM ${BASE_IMAGE} as builder

# Install Poetry
ARG POETRY_HOME=/opt/poetry
ARG POETRY_VERSION=1.6.1

# Required for building packages for arm64 arch
# RUN apt-get update && apt-get install -y --no-install-recommends python3-dev build-essential

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip config set global.timeout 1800 && pip config set global.retries 10
RUN python3 -m venv ${POETRY_HOME} && ${POETRY_HOME}/bin/python3 -m pip install --upgrade pip && ${POETRY_HOME}/bin/pip install poetry==${POETRY_VERSION}
ENV PATH="$PATH:${POETRY_HOME}/bin"
ENV POETRY_REQUESTS_TIMEOUT=600
ENV POETRY_RETRIES=10

# Activate virtual env
ARG VENV_PATH
ENV VIRTUAL_ENV=${VENV_PATH}
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# COPY document-qa/pyproject.toml document-qa/poetry.lock document-qa/
COPY document-qa/pyproject.toml document-qa/
RUN cd document-qa && poetry install --no-root --no-interaction --no-cache --with qa,test
COPY document-qa document-qa
RUN cd document-qa && poetry install --no-interaction --no-cache --with qa,test


FROM ${BASE_IMAGE} as prod

# Activate virtual env
ARG VENV_PATH
ENV VIRTUAL_ENV=${VENV_PATH}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

RUN useradd qateam -m -u 1000 -d /home/qateam

COPY --from=builder --chown=qateam:qateam ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=builder document-qa document-qa

USER 1000

RUN cd document-qa
# ENTRYPOINT ["python", "-m", "qaserver"]