FROM python:3.12-slim AS builder

WORKDIR /build

COPY . .
RUN pip wheel --no-cache-dir --wheel-dir /wheels .

FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/jimstrang/cloudflare-prometheus-exporter"

ENV PYTHONUNBUFFERED=1 \
	EXPORTER_PORT=9199

RUN useradd --create-home --shell /usr/sbin/nologin cfexporter \
	&& mkdir -p /config \
	&& chown cfexporter:cfexporter /config

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl \
	&& rm -rf /wheels

USER cfexporter

EXPOSE 9199

ENTRYPOINT ["cfexpose"]
CMD ["export", "/config/config.yaml"]
