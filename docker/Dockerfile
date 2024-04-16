FROM python:3.8-slim

COPY . singer-tap-ga4/

RUN cd singer-tap-ga4

WORKDIR singer-tap-ga4

RUN pip install -e .

# Your application run command
ENTRYPOINT ["python", "./tap_google_analytics/tap.py"]
