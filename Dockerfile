FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends git bash \
    && rm -rf /var/lib/apt/lists/* \
    && git config --system --add safe.directory /game \
    && git config --system core.pager cat
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /game
CMD ["bash"]
