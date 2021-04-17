FROM python:3-slim
MAINTAINER steve@beeka.org

RUN	pip install --quiet --no-cache-dir beautifulsoup4
# matplotlib

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY --chown=appuser *.py ./
COPY --chown=appuser prices prices

ENV DATA_ROOT /opt/data

VOLUME /opt/data

CMD [ "python", "./service.py" ]
